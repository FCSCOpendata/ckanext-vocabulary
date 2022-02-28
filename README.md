## Ckanext-Vocabulary

UI to manage vocabulary and tags

## Installation

```sh
pip3 install -e git+https://github.com/datopian/ckanext-vocabulary.git#egg=ckanext-vocabulary
```

After installing the extension, `vocabulary`  should be added to the list of plugins

```
CKAN_PLUGIN = vocabulary
```

## USAGE

`/vocabulary/` : To view all vocabularies available

`/vocabulary/new`: To create new vocabularied and tags

`/vocabulary/<id>/read`: view a vocabulary and its tags

`/vocabulary/<id>/edit`: Edit vocabulary or delete vocabulary

`/vocabulary/<id>/tags/new`: Create new tag(s)

`/vocabulary/<vocab_id>/tag/<id>/delete`: To delete tag 