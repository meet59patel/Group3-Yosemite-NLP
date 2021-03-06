# Yosemite NLP

* Call assess_answer() present in similarity_v1.py to get marks.
* Function parameters are reference answer, student answer and the maximum marks of the question.
Run Server:

```
$ export FLASK_APP=main.py
$ export FLASK_ENV=development
$ flask run
```

- Note: `chmod +x runserver.sh` before running script for the first time.
- similarity_v1 is based on the following [Research Paper](http://ijcset.net/docs/Volumes/Volume%209/ijcset2019090109.pdf).
