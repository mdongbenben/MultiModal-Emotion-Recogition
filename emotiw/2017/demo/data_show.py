# import cPickle as pickle
# f = open('path')
# info = pickle.load(f)
# print info   #show file

import joblib

pkl_load = joblib.load('../test_features_modelA_aug_det0_3.pkl')
for i,item in enumerate(pkl_load):
    print(len(item))