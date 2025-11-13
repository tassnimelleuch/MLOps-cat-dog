import os
from pathlib import Path
import csv
import numpy as np
from PIL import Image

try:
    from tensorflow.keras.models import load_model
except Exception:
    # Defer import error until runtime so static checks pass in environments
    # without TF installed.
    load_model = None


def _load_image(image_path, target_size):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr


def evaluate_model(model_path: Path, test_dir: Path, output_csv: Path = None):
    """Evaluate a binary cat/dog model on the test directory.

    Expects test_dir to contain two subfolders: 'cats' and 'dogs'.
    The function supports a model that outputs either a single sigmoid
    probability (shape (1,)) or a two-element softmax.
    """
    if load_model is None:
        raise RuntimeError('TensorFlow is not available in this environment.')

    if not model_path.exists():
        raise FileNotFoundError(f'Model not found: {model_path}')

    model = load_model(str(model_path))

    # Infer target size from model input or fall back to (150,150)
    try:
        input_shape = model.input_shape
        # input_shape might be (None, height, width, channels)
        if len(input_shape) >= 3:
            target_size = (input_shape[1] or 150, input_shape[2] or 150)
        else:
            target_size = (150, 150)
    except Exception:
        target_size = (150, 150)

    classes = ['cats', 'dogs']
    totals = 0
    correct = 0
    tp = fp = tn = fn = 0
    rows = []

    for label_idx, cls in enumerate(classes):
        cls_dir = test_dir / cls
        if not cls_dir.exists():
            print(f'Warning: test class folder not found: {cls_dir}')
            continue

        for img_path in sorted(cls_dir.iterdir()):
            if img_path.is_dir():
                continue
            try:
                x = _load_image(img_path, target_size)
            except Exception as e:
                print(f'Could not load image {img_path}: {e}')
                continue

            x_input = np.expand_dims(x, axis=0)
            preds = model.predict(x_input)

            # handle sigmoid output (shape (1,1) or (1,)) or softmax (1,2)
            if preds.ndim == 2 and preds.shape[1] == 1:
                prob = float(preds[0, 0])
                pred_label = 1 if prob >= 0.5 else 0
                score = prob
            elif preds.ndim == 2 and preds.shape[1] >= 2:
                probs = preds[0]
                pred_label = int(np.argmax(probs))
                score = float(probs[pred_label])
            else:
                # fallback: try flatten
                prob = float(np.ravel(preds)[0])
                pred_label = 1 if prob >= 0.5 else 0
                score = prob

            is_correct = (pred_label == label_idx)
            totals += 1
            if is_correct:
                correct += 1

            # update confusion counts: positive class = 'dogs' (index 1)
            if label_idx == 1 and pred_label == 1:
                tp += 1
            elif label_idx == 0 and pred_label == 1:
                fp += 1
            elif label_idx == 0 and pred_label == 0:
                tn += 1
            elif label_idx == 1 and pred_label == 0:
                fn += 1

            rows.append({
                'image': str(img_path),
                'true': cls,
                'predicted': classes[pred_label],
                'score': score,
                'correct': is_correct,
            })

    accuracy = correct / totals if totals else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    print('Evaluation results:')
    print(f'  Total images: {totals}')
    print(f'  Accuracy: {accuracy:.4f}')
    print(f'  Precision (dogs): {precision:.4f}')
    print(f'  Recall (dogs): {recall:.4f}')
    print(f'  F1 (dogs): {f1:.4f}')
    print('  Confusion matrix:')
    print(f'    TP={tp}  FP={fp}')
    print(f'    FN={fn}  TN={tn}')

    if output_csv:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with open(output_csv, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=['image', 'true', 'predicted', 'score', 'correct'])
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        print(f'Predictions written to: {output_csv}')

    return {
        'total': totals,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn,
    }


if __name__ == '__main__':
    # Default paths relative to repository root
    repo_root = Path(__file__).resolve().parents[2]
    model_path = repo_root / 'models' / 'cat_dog_model.h5'
    test_dir = repo_root / 'data' / 'test_set' / 'test_set'
    out_csv = repo_root / 'models' / 'evaluation_predictions.csv'

    try:
        metrics = evaluate_model(model_path, test_dir, out_csv)
    except Exception as e:
        print(f'Error during evaluation: {e}')
        raise