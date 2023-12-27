# 用户的基本操作，蓝图的定义，用户功能模块的定义
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, user_status_true, user_status_false, user_status_all
import shap
# import xgboost
import numpy as np
import pandas as pd
import json
import base64
from io import BytesIO
import io
import matplotlib.pyplot as plt
import matplotlib  # 添加这一行
matplotlib.use('Agg')
import seaborn as sns
frontshapapp = Blueprint('frontshapapp', __name__)

# 获取力图
@frontshapapp.route('/api/front/shap/gettestshap', methods=['get'])
def get_test_shap():
    # import shap
    # import xgboost
    # import matplotlib.pyplot as plt
    #
    # # 加载数据和模型
    # X, y = shap.datasets.diabetes()
    # model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)
    #
    # # 创建解释器
    # explainer = shap.TreeExplainer(model)
    #
    # # 计算SHAP值
    # shap_values = explainer.shap_values(X)
    #
    # # 创建AdditiveForceVisualizer对象
    # afv = shap.Explanation(X.iloc[:100, :], shap_values[:100, :], feature_names=X.columns)
    #
    # # 创建汇总图
    # afv.summary_plot()
    #
    # # 保存图像文件
    # plt.savefig('summary_plot.png')
    return '1111'


def _matplotlib_to_html(fig):
    """
    Convert a matplotlib figure to an HTML image tag.
    """
    # Save the figure to a PNG in memory.
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)

    # Encode the PNG as base64.
    data = base64.b64encode(buf.read()).decode('utf-8')

    # Create the HTML image tag.
    html = '<img src="data:image/png;base64,{}">'.format(data)

    return html
#绘制特征重要度图
@frontshapapp.route('/api/front/shap/summary_plot', methods=['get'])
def summary_plot():
    """
    Convert a matplotlib figure to an HTML image tag.
    """
    # Save the figure to a PNG in memory.

    import io
    import matplotlib.pyplot as plt
    import matplotlib  # 添加这一行
    matplotlib.use('Agg')
    import numpy as np
    import pandas as pd
    # 导入数据集，划分特征和标签
    df = pd.read_csv('process_heart.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    # 划分训练集和测试集
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # 构建随机森林模型
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(max_depth=5, n_estimators=100)
    model.fit(X_train, y_train)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    print(shap_values)
    shap.summary_plot(shap_values[1], X_test, plot_type="bar")
    # plt.savefig('myplot3.png')
    sio = io.BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + data
    context = {
         'img': src,
    }
    # plt.savefig('myplot1.png')
    return context
    # return '2222'

# 绘制热力图
@frontshapapp.route('/api/front/shap/heat_map', methods=['get'])
def heat_map():
    # 导入数据集，划分特征和标签
    df = pd.read_csv('process_heart.csv')

    #figsize 绘图的大小
    plt.figure(figsize=(10, 10))
    # df.corr() #生成特征性两两相关性的矩阵
    #绘制两两相关性的热力图，annot=True 表示把数字写在图标上， fmt='.1f'表示保留一位小数，square=True表示图形为方形
    sns.heatmap(df.corr(), annot=True, fmt='.1f', square=True)
    plt.savefig('myplot4.png')
    sio = io.BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + data
    context = {
        'img': src,
    }
    return context

# 绘制散点图
@frontshapapp.route('/api/front/shap/scatter', methods=['get'])
def scatter():
    # 导入数据集，划分特征和标签
    df = pd.read_csv('process_heart.csv')

    plt.scatter(x=df.age[df.target == 1], y=df.max_heart_rate_achieved[(df.target == 1)], c="red")
    plt.scatter(x=df.age[df.target == 0], y=df.max_heart_rate_achieved[(df.target == 0)], c="blue")
    plt.legend(["Disease", "Not Disease"])
    plt.xlabel("Age")
    plt.ylabel("Maximum Heart Rate")
    plt.savefig('myplot1.png')
    # sio = io.BytesIO()
    # plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    # data = base64.encodebytes(sio.getvalue()).decode()
    # src = 'data:image/png;base64,' + data
    # context = {
    #     'img': src,
    # }
    return '222'
    # return context


# 绘制附加力图
@frontshapapp.route('/api/front/shap/force_plot', methods=['get'])
def force_plot():
    # 导入数据集，划分特征和标签
    df = pd.read_csv('process_heart.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    # 划分训练集和测试集
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # 构建随机森林模型
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(max_depth=5, n_estimators=100)
    model.fit(X_train, y_train)
    # 获得定性测试结果
    y_pred = model.predict(X_test)
    # 获得定量测试结果
    y_pred_proba = model.predict_proba(X_test)
    explainer = shap.TreeExplainer(model)
    # 计算测试样本里每一个样本特征的shap值
    shap_values = explainer.shap_values(X_test)
    # 选取完整数据集中索引为idx的样本
    idx = 126

    patient = X.iloc[idx, :]
    patient_df = X.loc[idx:idx]
    model_predict_proba = model.predict_proba(patient_df)[0][1]
    # print('{}号病人的真实标签是 {} ，模型预测为 {:.2f} '.format(idx, bool(y_test[idx]), model_predict_proba))
    shap_values_patient = explainer.shap_values(patient)
    shap.force_plot(explainer.expected_value[1], shap_values_patient[1], patient,matplotlib=True,show=False)
    plt.savefig('myplot2.png')
    sio = io.BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + data
    context = {
        'img': src,
    }

    return context