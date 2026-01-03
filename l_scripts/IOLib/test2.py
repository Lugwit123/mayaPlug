# coding:utf-8
import sys
sys.path.append(r'D:\TD_Depot\plug_in\python2_lib')
from flask import Flask, render_template
import os

template_folder_path = u'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\plug-ins'
app = Flask(__name__, template_folder=template_folder_path)

@app.route('/')
def index():
    return render_template(u'index.html', title=u'首页', name=u'用户')

if __name__ == '__main__':
    app.run(debug=True)