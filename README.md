### 気分 dish のバックエンドのリポジトリです。

### フォルダ構成
```
code
- db_create.py(データベースを作るプログラム)
- app.py(DB とフロントの操作をするためのプログラム)
- kibun-dish.db(データベース)
- templates
  - index.html
```
### POST・GET routing
```
/food
/feel
/relation
```

### GET return
```
/food
  [{
    'id':n,
    'name':name
  }]
/feel
  [{
    'id':n,
    'name':name
  }]
/relation
  [{
    'id':n,
    'evaluation':n,
    'food':{'id':n, 'name':name},
    'feel':{'id':n, 'name':name},
  }]

*nは任意の自然数
```

### POST method wanted
```
[{
  'food_name':name,
  'feel_name':name,
  'evaluation':n
}]

*nは任意の自然数
```
