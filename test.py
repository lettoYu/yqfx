from utils import load_model, extend_maps
from data import build_corpus
from evaluating import Metrics

LSTM_MODEL_PATH = './ckpts/lstm.pkl'
CNN_MODEL_PATH = './ckpts/cnn.pkl'
REMOVE_O = False  # 在评估的时候是否去除O标记

def prLSTM(text):
    train_word_lists, train_tag_lists, word2id, tag2id, word_emb =build_corpus("train", make_vocab = True)
    hmm_model = load_model(LSTM_MODEL_PATH)
    train_word_lists = [list(text)]
    pred_tag_lists, test_tag_lists = hmm_model.test(
        train_word_lists, train_tag_lists, word2id, tag2id)
    i = 0
    newtext = ''
    while (i < len(pred_tag_lists[0])):
        if (pred_tag_lists[0][i] == 'O'):
            i += 1
        else:
            entity = ''
            while (pred_tag_lists[0][i] != 'O'):
                entity = entity + text[i]
                i += 1
            newtext += entity+'-'+pred_tag_lists[0][i-1].split('-')[1][:-1]+'-'+pred_tag_lists[0][i-1][len(pred_tag_lists[0][i-1])-1]+'\n'
    return newtext
    
def prCNN(text):
    train_word_lists, train_tag_lists, word2id, tag2id, word_emb =build_corpus("train", make_vocab = True)
    hmm_model = load_model(CNN_MODEL_PATH)
    train_word_lists = [list(text)]
    pred_tag_lists, test_tag_lists = hmm_model.test(
        train_word_lists, train_tag_lists, word2id, tag2id)
    i = 0
    newtext = ''
    while (i < len(pred_tag_lists[0])):
        if (pred_tag_lists[0][i] == 'O'):
            i += 1
        else:
            entity = ''
            while (pred_tag_lists[0][i] != 'O'):
                entity = entity + text[i]
                i += 1
            newtext += entity+'-'+pred_tag_lists[0][i-1].split('-')[1][:-1]+'-'+pred_tag_lists[0][i-1][len(pred_tag_lists[0][i-1])-1]+'\n'
    return newtext

def main():
    print("读取数据...")
    train_word_lists, train_tag_lists, word2id, tag2id, word_emb =build_corpus("train", make_vocab = True)
    dev_word_lists, dev_tag_lists = build_corpus("dev", make_vocab=False)
    test_word_lists, test_tag_lists = build_corpus("test", make_vocab=False)
    print("加载并评估CNN模型...")
    CNN_model = load_model(CNN_MODEL_PATH)
    pred_tag_lists, test_tag_lists = CNN_model.test(
        test_word_lists, test_tag_lists, word2id, tag2id)
    metrics = Metrics(test_tag_lists, pred_tag_lists, remove_O=False)
    metrics.report_scores()
    metrics.report_confusion_matrix()

if __name__ == "__main__":
    main()