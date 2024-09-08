from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import pickle
import os

filepath=os.path.dirname(os.path.abspath(__file__))


def predict():

    os.makedirs(f"{filepath}/data/",exist_ok=True)
    os.makedirs(f"{filepath}/model/",exist_ok=True)

    CLASSES=["빙어","도미"]

    l=float(input("🆕 물고기의 길이를 입력하세요(cm) : "))
    w=float(input("🆕 물고기의 무게를 입력하세요(kg) : "))

    ## 데이터가 있는지
    if os.path.exists(f"{filepath}/data/fish.csv"):
        df = pd.read_csv(f"{filepath}/data/fish.csv")
        df = df[["Length","Weight","Label"]]
    else:
        df = pd.DataFrame({"Length":[],"Weight":[],"Label":[]})
    #print(df)

    ## 모델이 있는지
    if os.path.exists(f"{filepath}/model/model.pkl"):
        with open(f"{filepath}/model/model.pkl", "rb") as f:
            knn=pickle.load(f)
        pred=knn.predict([[l,w]])
        pred=CLASSES[int(pred)]
    else:
        pred="도미"

    while True:
        rst = input(f"🆕 {pred}가 맞나요? (y/n)")
        if rst.lower()=="y":
            df=pd.concat([df,pd.DataFrame({"Length":[l],"Weight":[w],"Label":[pred]})])
            break
        elif rst.lower()=="n":
            df=pd.concat([df,pd.DataFrame({"Length":[l],"Weight":[w],"Label":[CLASSES[1-CLASSES.index(pred)]]})])
            break
        else:
            print("⛔ y 또는 n으로 답해주세요.")
            continue
    #print(df)
    df.to_csv(f"{filepath}/data/fish.csv")

    return df


def train(data):
    print("🆕 훈련을 시작합니다.")
    #print(data)

    import numpy as np
    import time
    from datetime import datetime

    t=time.time()
    df=data

    n=len(df)

    if n<2:
        print("⛔ 충분한 데이터가 없습니다.")
        return None
    elif n<5:
        knn=KNeighborsClassifier(n_neighbors=n)
    else:
        knn=KNeighborsClassifier(n_neighbors=5)
    
    fish_data=np.column_stack( [list(map(float,df["Length"].to_list())), list(map(float,df["Weight"].to_list()))] )
    fish_label=df["Label"].apply(lambda x:int(x=="도미")).to_list()

    mu = np.mean(fish_data,axis=0)
    std = np.std(fish_data,axis=0)

    z = (fish_data - mu) / std

    knn.fit(z,fish_label)
    
    with open(f"{filepath}/model/model.pkl", "wb") as f:
        knn=pickle.dump(knn,f)

    print(f"🆕 훈련을 종료합니다. (훈련시간 : {datetime.fromtimestamp(time.time()-t).second}초)")

    return knn
    

def get_pkl():
    #os.path.expanduser("~")

    if os.path.exists(f"{filepath}/model/model.pkl"):
        path=input("🆕 pkl파일을 저장할 경로를 입력해주세요 : ")
        os.system(f"cp {filepath}/model/model.pkl {path}/model.pkl")
        print(f"🆕 저장이 완료되었습니다.(저장경로 : {path}/model.pkl)")
    else:
        print("⛔ 훈련된 pkl파일이 없습니다.\n⛔ 모델 훈련 후 다시 확인해주세요.")

def show_data():
    if os.path.exists(f"{filepath}/data/fish.csv"):
        df = pd.read_csv(f"{filepath}/data/fish.csv")
        df = df[["Length","Weight","Label"]]
        print(df)
    else:
        print("⛔ 저장된 데이터가 없습니다.")

def run():
    df = predict()
    train(df)