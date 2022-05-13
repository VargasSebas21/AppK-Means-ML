import pandas as pd
import numpy as np
import matplotlib
import shutil, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
import base64
from flask import jsonify, request

class Kmeans:
  dataframe = pd.read_excel(r"1. TRANSACCIONES SIN ATIPICOS.xlsx")
  return_images = []
  kmeans = None

  def save_graph(self, name: str):
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.8, 
                    hspace=0.8)
    plt.savefig(f'temp/{name}.jpg')
    self.return_images.append(name)

  def convert_to_base_64(self, name):
    with open(f'temp/{name}.jpg', 'rb') as img:
      img_str = base64.b64encode(img.read()).decode()
      return img_str

  def predict(self):
    data = request.args.get('data')
    new_data = [int(d) for d in data.split(',')]
    X_new = np.array([new_data])
    new_label = self.kmeans.predict(X_new)
    return jsonify({
      "response": new_label.tolist()
    })

  def kmeans(self):
    self.dataframe.drop(['CANAL'], 1).hist()
    self.save_graph('hist') 

    sb.pairplot(self.dataframe.dropna(), hue='CANAL', height=2, vars=['N_CREDITO', 'N_DEBITO'], kind='scatter')
    self.save_graph('pairplot')

    X = np.array(self.dataframe[["N_CREDITO", "N_DEBITO"]])
    y = np.array(self.dataframe['CANAL'])

    Nc = range(1, 20)
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
    plt.clf()
    plt.cla()
    plt.plot(Nc, score)
    plt.xlabel('Numero de clusters')
    plt.ylabel('Puntaje')
    plt.title('Elbow Curve')
    self.save_graph('Elbow Curve')

    self.kmeans = KMeans(n_clusters=8).fit(X)

    labels = self.kmeans.predict(X)

    C = self.kmeans.cluster_centers_
    colores=['red','green','blue','cyan','yellow', 'purple', 'orange', 'pink']
    asignar=[]
    for row in labels:
      asignar.append(colores[row])
    
    val1 = self.dataframe['N_CREDITO'].values
    val2 = self.dataframe['N_DEBITO'].values

    plt.clf()
    plt.cla()
    plt.scatter(val1, val2, c=asignar, s=70)
    plt.scatter(C[:, 0], C[:, 1], marker='*', c=colores, s=1000)
    self.save_graph('scatter')

    response = [{
      "name": name,
      "image": self.convert_to_base_64(name)
    } for name in self.return_images]

    return jsonify(response)