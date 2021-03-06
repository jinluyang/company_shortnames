# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
require CRF++
将此文件夹放在CRF++的根目录下
linux运行
'''
import re
import jieba
import jieba.analyse
import MySQLdb
import os
import codecs

def remove_bracket(x):#utf8
    eng_brk = re.compile('\(.*?\)')
    chi_brk = re.compile('\（.*?\）')
    brk = re.compile('\【.*?\】')
    x = eng_brk.sub('', x)
    x = chi_brk.sub('', x)
    x = brk.sub('', x)
    return x
    
end_allnormal=['部','公司','店','团','中心','馆','园','业','厂','大区','网','办事处','社','基地','科技','办公室','院','商','场',
'联盟','所','实业','学校','铺','世家','代理','室','城','超市','加盟商','行','辅导班','场','传媒','协会','厂家','个体经营',
'库','处','家纺','坊','代购','论坛','培训','站','1','）','吧','厅','矿','影像','金属','点',')','房','庄','楼','客栈','队','公寓']
places=[ u'\u5b89\u5fbd', u'\u798f\u5efa', u'\u7518\u8083', u'\u5e7f\u4e1c', u'\u8d35\u5dde', u'\u6cb3\u5317', u'\u9ed1\u9f99\u6c5f', u'\u6cb3\u5357', u'\u6e56\u5317', u'\u6e56\u5357', u'\u5409\u6797', u'\u6c5f\u897f', u'\u6c5f\u82cf', u'\u8fbd\u5b81', u'\u5c71\u4e1c', u'\u9655\u897f', u'\u5c71\u897f', u'\u56db\u5ddd', u'\u4e91\u5357', u'\u6d59\u6c5f', u'\u9752\u6d77', u'\u6d77\u5357', u'\u5e7f\u897f\u58ee\u65cf', u'\u5185\u8499\u53e4', u'\u5b81\u590f\u56de\u65cf', u'\u897f\u85cf', u'\u65b0\u7586\u7ef4\u543e\u5c14', u'\u53f0\u6e7e',u'\u57ce\u5e02', u'\u5317\u4eac', u'\u5929\u6d25', u'\u4e0a\u6d77', u'\u91cd\u5e86', u'\u5408\u80a5', u'\u5bbf\u5dde', u'\u6dee\u5317', u'\u961c\u9633', u'\u868c\u57e0', u'\u6dee\u5357', u'\u6ec1\u5dde', u'\u9a6c\u978d\u5c71', u'\u829c\u6e56', u'\u94dc\u9675', u'\u5b89\u5e86', u'\u9ec4\u5c71', u'\u516d\u5b89', u'\u6c60\u5dde', u'\u5ba3\u57ce', u'\u4eb3\u5dde', u'\u754c\u9996', u'\u660e\u5149', u'\u5929\u957f', u'\u6850\u57ce', u'\u5b81\u56fd', u'\u5de2\u6e56', u'\u53a6\u95e8', u'\u798f\u5dde', u'\u5357\u5e73', u'\u4e09\u660e', u'\u8386\u7530', u'\u6cc9\u5dde', u'\u6f33\u5dde', u'\u9f99\u5ca9', u'\u5b81\u5fb7', u'\u798f\u6e05', u'\u957f\u4e50', u'\u90b5\u6b66', u'\u6b66\u5937\u5c71', u'\u5efa\u74ef', u'\u5efa\u9633', u'\u6c38\u5b89', u'\u77f3\u72ee', u'\u664b\u6c5f', u'\u5357\u5b89', u'\u9f99\u6d77', u'\u6f33\u5e73', u'\u798f\u5b89', u'\u798f\u9f0e', u'\u5170\u5dde', u'\u5609\u5cea\u5173', u'\u91d1\u660c', u'\u767d\u94f6', u'\u5929\u6c34', u'\u9152\u6cc9', u'\u5f20\u6396', u'\u6b66\u5a01', u'\u5e86\u9633', u'\u5e73\u51c9', u'\u5b9a\u897f', u'\u9647\u5357', u'\u7389\u95e8', u'\u6566\u714c', u'\u4e34\u590f', u'\u5408\u4f5c', u'\u5e7f\u5dde', u'\u6df1\u5733', u'\u6e05\u8fdc', u'\u97f6\u5173', u'\u6cb3\u6e90', u'\u6885\u5dde', u'\u6f6e\u5dde', u'\u6c55\u5934', u'\u63ed\u9633', u'\u6c55\u5c3e', u'\u60e0\u5dde', u'\u4e1c\u839e', u'\u73e0\u6d77', u'\u4e2d\u5c71', u'\u6c5f\u95e8', u'\u4f5b\u5c71', u'\u8087\u5e86', u'\u4e91\u6d6e', u'\u9633\u6c5f', u'\u8302\u540d', u'\u6e5b\u6c5f', u'\u4ece\u5316', u'\u589e\u57ce', u'\u82f1\u5fb7', u'\u8fde\u5dde', u'\u4e50\u660c', u'\u5357\u96c4', u'\u5174\u5b81', u'\u666e\u5b81', u'\u9646\u4e30', u'\u6069\u5e73', u'\u53f0\u5c71', u'\u5f00\u5e73', u'\u9e64\u5c71', u'\u9ad8\u8981', u'\u56db\u4f1a', u'\u7f57\u5b9a', u'\u9633\u6625', u'\u5316\u5dde', u'\u4fe1\u5b9c', u'\u9ad8\u5dde', u'\u5434\u5ddd', u'\u5ec9\u6c5f', u'\u96f7\u5dde', u'\u8d35\u9633', u'\u516d\u76d8\u6c34', u'\u9075\u4e49', u'\u5b89\u987a', u'\u6bd5\u8282', u'\u94dc\u4ec1', u'\u6e05\u9547', u'\u8d64\u6c34', u'\u4ec1\u6000', u'\u51ef\u91cc', u'\u90fd\u5300', u'\u5174\u4e49', u'\u798f\u6cc9', u'\u77f3\u5bb6\u5e84', u'\u90af\u90f8', u'\u5510\u5c71', u'\u4fdd\u5b9a', u'\u79e6\u7687\u5c9b', u'\u90a2\u53f0', u'\u5f20\u5bb6\u53e3', u'\u627f\u5fb7', u'\u6ca7\u5dde', u'\u5eca\u574a', u'\u8861\u6c34', u'\u8f9b\u96c6', u'\u85c1\u57ce', u'\u664b\u5dde', u'\u65b0\u4e50', u'\u9e7f\u6cc9', u'\u9075\u5316', u'\u8fc1\u5b89', u'\u9738\u5dde', u'\u4e09\u6cb3', u'\u5b9a\u5dde', u'\u6dbf\u5dde', u'\u5b89\u56fd', u'\u9ad8\u7891\u5e97', u'\u6cca\u5934', u'\u4efb\u4e18', u'\u9ec4\u9a85', u'\u6cb3\u95f4', u'\u5180\u5dde', u'\u6df1\u5dde', u'\u5357\u5bab', u'\u6c99\u6cb3', u'\u6b66\u5b89', u'\u54c8\u5c14\u6ee8', u'\u9f50\u9f50\u54c8\u5c14', u'\u9ed1\u6cb3', u'\u5927\u5e86', u'\u4f0a\u6625', u'\u9e64\u5c97', u'\u4f73\u6728\u65af', u'\u53cc\u9e2d\u5c71', u'\u4e03\u53f0\u6cb3', u'\u9e21\u897f', u'\u7261\u4e39\u6c5f', u'\u7ee5\u5316', u'\u53cc\u57ce', u'\u5c1a\u5fd7', u'\u4e94\u5e38', u'\u963f\u57ce', u'\u8bb7\u6cb3', u'\u5317\u5b89', u'\u4e94\u5927\u8fde\u6c60', u'\u94c1\u529b', u'\u540c\u6c5f', u'\u5bcc\u9526', u'\u864e\u6797', u'\u5bc6\u5c71', u'\u7ee5\u82ac\u6cb3', u'\u6d77\u6797', u'\u5b81\u5b89', u'\u5b89\u8fbe', u'\u8087\u4e1c', u'\u6d77\u4f26', u'\u90d1\u5dde', u'\u5f00\u5c01', u'\u6d1b\u9633', u'\u5e73\u9876\u5c71', u'\u5b89\u9633', u'\u9e64\u58c1', u'\u65b0\u4e61', u'\u7126\u4f5c', u'\u6fee\u9633', u'\u8bb8\u660c', u'\u6f2f\u6cb3', u'\u4e09\u95e8\u5ce1', u'\u5357\u9633', u'\u5546\u4e18', u'\u5468\u53e3', u'\u9a7b\u9a6c\u5e97', u'\u4fe1\u9633', u'\u6d4e\u6e90', u'\u5de9\u4e49', u'\u9093\u5dde', u'\u6c38\u57ce', u'\u6c5d\u5dde', u'\u8365\u9633', u'\u65b0\u90d1', u'\u767b\u5c01', u'\u65b0\u5bc6', u'\u5043\u5e08', u'\u5b5f\u5dde', u'\u6c81\u9633', u'\u536b\u8f89', u'\u8f89\u53bf', u'\u6797\u5dde', u'\u79b9\u5dde', u'\u957f\u845b', u'\u821e\u94a2', u'\u4e49\u9a6c', u'\u7075\u5b9d', u'\u9879\u57ce', u'\u6b66\u6c49', u'\u5341\u5830', u'\u8944\u6a0a', u'\u8346\u95e8', u'\u5b5d\u611f', u'\u9ec4\u5188', u'\u9102\u5dde', u'\u9ec4\u77f3', u'\u54b8\u5b81', u'\u8346\u5dde', u'\u5b9c\u660c', u'\u968f\u5dde', u'\u4ed9\u6843', u'\u5929\u95e8', u'\u6f5c\u6c5f', u'\u4e39\u6c5f\u53e3', u'\u8001\u6cb3\u53e3', u'\u67a3\u9633', u'\u5b9c\u57ce', u'\u949f\u7965', u'\u6c49\u5ddd', u'\u5e94\u57ce', u'\u5b89\u9646', u'\u5e7f\u6c34', u'\u9ebb\u57ce', u'\u6b66\u7a74', u'\u5927\u51b6', u'\u8d64\u58c1', u'\u77f3\u9996', u'\u6d2a\u6e56', u'\u677e\u6ecb', u'\u5b9c\u90fd', u'\u679d\u6c5f', u'\u5f53\u9633', u'\u6069\u65bd', u'\u5229\u5ddd', u'\u957f\u6c99', u'\u8861\u9633', u'\u5f20\u5bb6\u754c', u'\u5e38\u5fb7', u'\u76ca\u9633', u'\u5cb3\u9633', u'\u682a\u6d32', u'\u6e58\u6f6d', u'\u90f4\u5dde', u'\u6c38\u5dde', u'\u90b5\u9633', u'\u6000\u5316', u'\u5a04\u5e95', u'\u8012\u9633', u'\u5e38\u5b81', u'\u6d4f\u9633', u'\u6d25\u5e02', u'\u6c85\u6c5f', u'\u6c68\u7f57', u'\u4e34\u6e58', u'\u91b4\u9675', u'\u6e58\u4e61', u'\u97f6\u5c71', u'\u8d44\u5174', u'\u6b66\u5188', u'\u6d2a\u6c5f', u'\u51b7\u6c34\u6c5f', u'\u6d9f\u6e90', u'\u5409\u9996', u'\u957f\u6625', u'\u5409\u6797\u5e02', u'\u767d\u57ce', u'\u677e\u539f', u'\u56db\u5e73', u'\u8fbd\u6e90', u'\u901a\u5316', u'\u767d\u5c71', u'\u5fb7\u60e0', u'\u4e5d\u53f0', u'\u6986\u6811', u'\u78d0\u77f3', u'\u86df\u6cb3', u'\u6866\u7538', u'\u8212\u5170', u'\u6d2e\u5357', u'\u5927\u5b89', u'\u53cc\u8fbd', u'\u516c\u4e3b\u5cad', u'\u6885\u6cb3\u53e3', u'\u96c6\u5b89', u'\u4e34\u6c5f', u'\u5ef6\u5409', u'\u56fe\u4eec', u'\u6566\u5316', u'\u73f2\u6625', u'\u9f99\u4e95', u'\u548c\u9f99', u'\u5357\u660c', u'\u4e5d\u6c5f', u'\u666f\u5fb7\u9547', u'\u9e70\u6f6d', u'\u65b0\u4f59', u'\u840d\u4e61', u'\u8d63\u5dde', u'\u4e0a\u9976', u'\u629a\u5dde', u'\u5b9c\u6625', u'\u5409\u5b89', u'\u745e\u660c', u'\u4e50\u5e73', u'\u745e\u91d1', u'\u5357\u5eb7', u'\u5fb7\u5174', u'\u4e30\u57ce', u'\u6a1f\u6811', u'\u9ad8\u5b89', u'\u4e95\u5188\u5c71', u'\u8d35\u6eaa', u'\u5357\u4eac', u'\u5f90\u5dde', u'\u8fde\u4e91\u6e2f', u'\u5bbf\u8fc1', u'\u6dee\u5b89', u'\u76d0\u57ce', u'\u626c\u5dde', u'\u6cf0\u5dde', u'\u5357\u901a', u'\u9547\u6c5f', u'\u5e38\u5dde', u'\u65e0\u9521', u'\u82cf\u5dde', u'\u6c5f\u9634', u'\u5b9c\u5174', u'\u90b3\u5dde', u'\u65b0\u6c82', u'\u91d1\u575b', u'\u6ea7\u9633', u'\u5e38\u719f', u'\u5f20\u5bb6\u6e2f', u'\u592a\u4ed3', u'\u6606\u5c71', u'\u5434\u6c5f', u'\u5982\u768b', u'\u6d77\u95e8', u'\u542f\u4e1c', u'\u5927\u4e30', u'\u4e1c\u53f0', u'\u9ad8\u90ae', u'\u4eea\u5f81', u'\u626c\u4e2d', u'\u53e5\u5bb9', u'\u4e39\u9633', u'\u5174\u5316', u'\u59dc\u5830', u'\u6cf0\u5174', u'\u9756\u6c5f', u'\u6c88\u9633', u'\u5927\u8fde', u'\u671d\u9633', u'\u961c\u65b0', u'\u94c1\u5cad', u'\u629a\u987a', u'\u672c\u6eaa', u'\u8fbd\u9633', u'\u978d\u5c71', u'\u4e39\u4e1c', u'\u8425\u53e3', u'\u76d8\u9526', u'\u9526\u5dde', u'\u846b\u82a6\u5c9b', u'\u65b0\u6c11', u'\u74e6\u623f\u5e97', u'\u666e\u5170\u5e97', u'\u5e84\u6cb3', u'\u5317\u7968', u'\u51cc\u6e90', u'\u8c03\u5175\u5c71', u'\u5f00\u539f', u'\u706f\u5854', u'\u6d77\u57ce', u'\u51e4\u57ce', u'\u4e1c\u6e2f', u'\u5927\u77f3\u6865', u'\u76d6\u5dde', u'\u51cc\u6d77', u'\u5317\u5b81', u'\u5174\u57ce', u'\u6d4e\u5357', u'\u9752\u5c9b', u'\u804a\u57ce', u'\u5fb7\u5dde', u'\u4e1c\u8425', u'\u6dc4\u535a', u'\u6f4d\u574a', u'\u70df\u53f0', u'\u5a01\u6d77', u'\u65e5\u7167', u'\u4e34\u6c82', u'\u67a3\u5e84', u'\u6d4e\u5b81', u'\u6cf0\u5b89', u'\u83b1\u829c', u'\u6ee8\u5dde', u'\u83cf\u6cfd', u'\u7ae0\u4e18', u'\u80f6\u5dde', u'\u80f6\u5357', u'\u5373\u58a8', u'\u5e73\u5ea6', u'\u83b1\u897f', u'\u4e34\u6e05', u'\u4e50\u9675', u'\u79b9\u57ce', u'\u5b89\u4e18', u'\u660c\u9091', u'\u9ad8\u5bc6', u'\u9752\u5dde', u'\u8bf8\u57ce', u'\u5bff\u5149', u'\u6816\u971e', u'\u6d77\u9633', u'\u9f99\u53e3', u'\u83b1\u9633', u'\u83b1\u5dde', u'\u84ec\u83b1', u'\u62db\u8fdc', u'\u6587\u767b', u'\u8363\u6210', u'\u4e73\u5c71', u'\u6ed5\u5dde', u'\u66f2\u961c', u'\u5156\u5dde', u'\u90b9\u57ce', u'\u65b0\u6cf0', u'\u80a5\u57ce', u'\u897f\u5b89', u'\u5ef6\u5b89', u'\u94dc\u5ddd', u'\u6e2d\u5357', u'\u54b8\u9633', u'\u5b9d\u9e21', u'\u6c49\u4e2d', u'\u6986\u6797', u'\u5546\u6d1b', u'\u5b89\u5eb7', u'\u97e9\u57ce', u'\u534e\u9634', u'\u5174\u5e73', u'\u592a\u539f', u'\u5927\u540c', u'\u6714\u5dde', u'\u9633\u6cc9', u'\u957f\u6cbb', u'\u664b\u57ce', u'\u5ffb\u5dde', u'\u5415\u6881', u'\u664b\u4e2d', u'\u4e34\u6c7e', u'\u8fd0\u57ce', u'\u53e4\u4ea4', u'\u6f5e\u57ce', u'\u9ad8\u5e73', u'\u539f\u5e73', u'\u5b5d\u4e49', u'\u6c7e\u9633', u'\u4ecb\u4f11', u'\u4faf\u9a6c', u'\u970d\u5dde', u'\u6c38\u6d4e', u'\u6cb3\u6d25', u'\u6210\u90fd', u'\u5e7f\u5143', u'\u7ef5\u9633', u'\u5fb7\u9633', u'\u5357\u5145', u'\u5e7f\u5b89', u'\u9042\u5b81', u'\u5185\u6c5f', u'\u4e50\u5c71', u'\u81ea\u8d21', u'\u6cf8\u5dde', u'\u5b9c\u5bbe', u'\u6500\u679d\u82b1', u'\u5df4\u4e2d', u'\u8fbe\u5dde', u'\u8d44\u9633', u'\u7709\u5c71', u'\u96c5\u5b89', u'\u5d07\u5dde', u'\u909b\u5d03', u'\u90fd\u6c5f\u5830', u'\u5f6d\u5dde', u'\u6c5f\u6cb9', u'\u4ec0\u90a1', u'\u5e7f\u6c49', u'\u7ef5\u7af9', u'\u9606\u4e2d', u'\u534e\u84e5', u'\u5ce8\u7709\u5c71', u'\u4e07\u6e90', u'\u7b80\u9633', u'\u897f\u660c', u'\u6606\u660e', u'\u66f2\u9756', u'\u7389\u6eaa', u'\u4e3d\u6c5f', u'\u662d\u901a', u'\u601d\u8305', u'\u4e34\u6ca7', u'\u4fdd\u5c71', u'\u5b89\u5b81', u'\u5ba3\u5a01', u'\u8292\u5e02', u'\u745e\u4e3d', u'\u5927\u7406', u'\u695a\u96c4', u'\u4e2a\u65e7', u'\u5f00\u8fdc', u'\u666f\u6d2a', u'\u676d\u5dde', u'\u5b81\u6ce2', u'\u6e56\u5dde', u'\u5609\u5174', u'\u821f\u5c71', u'\u7ecd\u5174', u'\u8862\u5dde', u'\u91d1\u534e', u'\u53f0\u5dde', u'\u6e29\u5dde', u'\u4e3d\u6c34', u'\u4e34\u5b89', u'\u5bcc\u9633', u'\u5efa\u5fb7', u'\u6148\u6eaa', u'\u4f59\u59da', u'\u5949\u5316', u'\u5e73\u6e56', u'\u6d77\u5b81', u'\u6850\u4e61', u'\u8bf8\u66a8', u'\u4e0a\u865e', u'\u5d4a\u5dde', u'\u6c5f\u5c71', u'\u5170\u6eaa', u'\u6c38\u5eb7', u'\u4e49\u4e4c', u'\u4e1c\u9633', u'\u4e34\u6d77', u'\u6e29\u5cad', u'\u745e\u5b89', u'\u4e50\u6e05', u'\u9f99\u6cc9', u'\u897f\u5b81', u'\u683c\u5c14\u6728', u'\u5fb7\u4ee4\u54c8', u'\u6d77\u53e3\u5e02', u'\u4e09\u4e9a\u5e02', u'\u6587\u660c\u5e02', u'\u743c\u6d77\u5e02', u'\u4e07\u5b81\u5e02', u'\u4e1c\u65b9\u5e02', u'\u510b\u5dde\u5e02', u'\u4e94\u6307\u5c71\u5e02', u'\u5357\u5b81', u'\u6842\u6797', u'\u67f3\u5dde', u'\u68a7\u5dde', u'\u8d35\u6e2f', u'\u7389\u6797', u'\u94a6\u5dde', u'\u5317\u6d77', u'\u9632\u57ce\u6e2f', u'\u5d07\u5de6', u'\u767e\u8272', u'\u6cb3\u6c60', u'\u6765\u5bbe', u'\u8d3a\u5dde', u'\u5c91\u6eaa', u'\u6842\u5e73', u'\u5317\u6d41', u'\u4e1c\u5174', u'\u51ed\u7965', u'\u5b9c\u5dde', u'\u5408\u5c71', u'\u547c\u548c\u6d69\u7279', u'\u5305\u5934', u'\u4e4c\u6d77', u'\u8d64\u5cf0', u'\u547c\u4f26\u8d1d\u5c14', u'\u901a\u8fbd', u'\u4e4c\u5170\u5bdf\u5e03', u'\u9102\u5c14\u591a\u65af', u'\u5df4\u5f66\u6dd6\u5c14', u'\u6ee1\u6d32\u91cc', u'\u624e\u5170\u5c6f', u'\u7259\u514b\u77f3', u'\u6839\u6cb3', u'\u989d\u5c14\u53e4\u7eb3', u'\u4e4c\u5170\u6d69\u7279', u'\u963f\u5c14\u5c71', u'\u970d\u6797\u90ed\u52d2', u'\u9521\u6797\u6d69\u7279', u'\u4e8c\u8fde\u6d69\u7279', u'\u4e30\u9547', u'\u94f6\u5ddd', u'\u77f3\u5634\u5c71', u'\u5434\u5fe0', u'\u4e2d\u536b', u'\u56fa\u539f', u'\u7075\u6b66', u'\u9752\u94dc\u5ce1', u'\u62c9\u8428', u'\u65e5\u5580\u5219', u'\u4e4c\u9c81\u6728\u9f50', u'\u514b\u62c9\u739b\u4f9d', u'\u77f3\u6cb3\u5b50', u'\u963f\u62c9\u5c14', u'\u56fe\u6728\u8212\u514b', u'\u4e94\u5bb6\u6e20', u'\u5317\u5c6f', u'\u5580\u4ec0', u'\u963f\u514b\u82cf', u'\u548c\u7530', u'\u5410\u9c81\u756a', u'\u54c8\u5bc6', u'\u963f\u56fe\u4ec0', u'\u535a\u4e50', u'\u660c\u5409', u'\u961c\u5eb7', u'\u7c73\u6cc9', u'\u5e93\u5c14\u52d2', u'\u4f0a\u5b81', u'\u594e\u5c6f', u'\u5854\u57ce', u'\u4e4c\u82cf', u'\u963f\u52d2\u6cf0', u'\u9999\u6e2f', u'\u6fb3\u95e8', u'\u672a\u6709\u7edf\u8ba1']

conn1 = MySQLdb.connect(host=,charset="utf8")
cursor1 = conn1.cursor()
conn2 = MySQLdb.connect(host=,charset="utf8")
cursor2 = conn2.cursor()

def washing(s):
    s=remove_bracket(s)
    l=jieba.lcut(s)
    for i in end_allnormal:
        if s.endswith(i):
            l=l[:-1]
            s=''.join(l)
    for i in places:
        if s.startswith(i):
            s=s[len(i):]
    if s.endswith('股份'):
        s=s[:-2]
    if s.endswith('有限责任'):
        s=s[:-4]
    if s.startswith('市'):
        s=s[1:]
    return s

sql="insert into shortnames (company_id,short,short2,crf,crfc1,crff2,crfmira) VALUES (%s,%s,%s,%s,%s,%s,%s)"
chunksize=500
size=1000
i=0


#os.system('bash exec.train')
while i*chunksize<size:
    param=[]
    cursor1.execute("select id,title from zd_company limit %s offset %s"% (chunksize,i*chunksize))
    bulk=cursor1.fetchall()
    f = codecs.open('short.test','w',encoding='utf8')
    for item in bulk:
        s1=washing(item[1])
        s2=jieba.analyse.extract_tags(s1,topK=1)
        if len(s2)==0:
            s2=None
        else:
            s2=s2[0]
        flag=[0]*len(item[1])
        itm=item[1]
        if ' ' in item[1]:
            itm=''.join(item[1].split(' '))
        if itm[:2] in places:
            flag[0]=flag[1]='P'
        for j in range(len(itm)):
            f.write(itm[j]+' '+'%s' %flag[j]+'\n')
        f.write('\n')
        param.append([item[0],s1,s2 ])

    f.close()
    
    os.system('bash exec.test')
    os.system('bash exec.test2')
    os.system('bash exec.test3')
    os.system('bash exec.test4')
    f=codecs.open('result.txt', encoding='utf-8')
    f2=codecs.open('result2.txt', encoding='utf-8')
    f3=codecs.open('result3.txt', encoding='utf-8')
    f4=codecs.open('result4.txt', encoding='utf-8')
    for ii in range(chunksize):
        for fil in [f,f2,f3,f4]:
            string=''
            while True:
                line=fil.readline()
                if line=='\n':
                    break
                list_line=line.split('\t')
                if list_line[2][0]=='T':
                    string=string+list_line[0][0]
            if len(string)<2:
                string=None
            param[ii].append(string)
        param[ii]=tuple(param[ii])
    f.close()
    f2.close()
    f3.close()
    f4.close()
    cursor2.executemany(sql,param)
    
    i+=1
    if i%100==0:
        print i*chunksize
conn1.close()
conn2.close()
