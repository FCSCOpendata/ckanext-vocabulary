from ast import Pass
from flask import Blueprint
import logging
import ckan.logic as logic
import ckan.lib.base as base
from ckan import model
from ckan.common import c, request, _, config, g
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.helpers as h



log = logging.getLogger(__name__)
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
check_access = logic.check_access
get_action = logic.get_action
clean_dict = logic.clean_dict
render = base.render
abort = base.abort
tuplize_dict = logic.tuplize_dict
parse_params = logic.parse_params

vocab_blueprint = Blueprint('vocabulary', __name__, url_prefix=u'/vocabulary')

def index():
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to create a group'))
    vocab_list = get_action('vocabulary_list')(context, {})
    return render('vocabulary/index.html', {'vocab_list': vocab_list})


def new():
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to create a group'))

    if request.method == 'POST':
        params = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        data_dict = {}
        data_dict['name'] = params['vocabulary']
        data_dict["name_translated-en"] = params['vocabulary']
        data_dict["name_translated-ar"] = params['vocabulary-ar']

        ar_tags = params['ar']
        en_tags = params['en']
        log.debug("tags")
        log.debug(params)
        log.debug(en_tags)
        if (ar_tags and en_tags) and (type(ar_tags) is list) :
            ztags = zip(en_tags, ar_tags)
            tags = []
            for tag in ztags:
                tag_dict = {}
                tag_dict['name'] = tag[0]
                tag_dict['name_translated-en'] = tag[0]
                tag_dict['name_translated-ar'] = tag[1]
                tags.append(tag_dict)
        else:
            tags = [{
                'name': en_tags,
                'name_translated-en': en_tags,
                'name_translated-ar': ar_tags
            }]
        data_dict['tags'] = tags
        create_vocab = get_action('vocabulary_create')(context, data_dict)
        return h.redirect_to(h.url_for('vocabulary_read', id=params['vocabulary']))

    return render('vocabulary/new.html', {})


def read(id):
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to create a group'))

    try:
        vocab = get_action("vocabulary_show")(context, {'id': id})
    except NotFound:
        abort(404, _('Vocabulary not found'))
    
    return render('vocabulary/read.html', {"vocab": vocab})


def edit(id):
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to edit vocabulary'))

    if request.method == "POST":
        params = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        
        get_action('vocabulary_update')(context, {'id': id, "name": params['vocabulary']})
        return h.redirect_to(h.url_for('vocabulary_read', id=id))

    vocab = get_action('vocabulary_show')(context, {'id': id})
    return render('vocabulary/edit.html', {"vocab": vocab})


def new_tags(id):
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to create new tags'))
    
    if request.method == "POST":
        params = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        ar_tags = params['ar']
        en_tags = params['en']

        if (ar_tags and en_tags) and (type(ar_tags) is list):
            ztags = zip(en_tags, ar_tags)
            tags = []
            for tag in ztags:
                tag_dict = {}
                tag_dict['name'] = tag[0]
                tag_dict['name_translated-en'] = tag[0]
                tag_dict['name_translated-ar'] = tag[1]
                tag_dict['vocabulary_id'] = id
                get_action('tag_create')(context, tag_dict)
        else:
            tag_dict = {
                'name': en_tags,
                'name_translated-en': en_tags,
                'name_translated-ar': ar_tags,
                'vocabulary_id': id
            }
            get_action('tag_create')(context, tag_dict)

        return h.redirect_to(h.url_for('vocabulary_read', id=id))
    try:
        vocab = get_action('vocabulary_show')(context, {'id': id})['name']
    except NotFound:
        abort(404, _('Vocabulary not found'))
    
    return render('vocabulary/new_tag.html', {'vocab_name': vocab})


def delete_tags(vocab_id, id):
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to delete tags'))

    if request.method == "POST":
        params = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        
        if "delete" in params:
            get_action('tag_delete')(context, {'id': id, 'vocabulary_id': vocab_id})
            return h.redirect_to(h.url_for('vocabulary_read', id=vocab_id))
        else:
            get_action('tag_update')(context, {'id': id, "name": params['tag'], 'vocabulary_id': vocab_id})
            return h.redirect_to(h.url_for('vocabulary_read', id=id))

    tag = get_action('tag_show')(context, {'id': id})
    vocab_name = get_action('vocabulary_show')(context, {'id': vocab_id})['name']
    return render('vocabulary/edit_tags.html', {"tag": tag, 'vocab_name': vocab_name})


def delete(id):
    context = {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
    if not c.userobj.sysadmin:
        base.abort(403, _(u'Unauthorized to delete vocabulary and tags'))
    
    if request.method == "POST":
        params = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        
        tags = get_action('vocabulary_show')(context, {'id': id})['tags']

        for tag in tags:
            get_action('tag_delete')(context, tag)
        get_action('vocabulary_delete')(context, {'id': id})
        return h.redirect_to(h.url_for('vocabulary.index'))

    vocab = get_action('vocabulary_show')(context, {'id': id})
    return render('vocabulary/confirm_delete.html', {"vocab": vocab})


vocab_blueprint.add_url_rule(u'/', methods=[u'GET'],view_func=index)
vocab_blueprint.add_url_rule(u'/new', methods=[u'GET', u'POST'],view_func=new)
vocab_blueprint.add_url_rule(u'/<id>/read', methods=[u'GET'],view_func=read)
vocab_blueprint.add_url_rule(u'/<id>/edit', methods=[u'GET', u'POST'],view_func=edit)
vocab_blueprint.add_url_rule(u'/<id>/tags/new', methods=[u'GET', u'POST'],view_func=new_tags)
vocab_blueprint.add_url_rule(u'/<vocab_id>/tag/<id>/delete', methods=[u'GET', u'POST'],view_func=delete_tags)
vocab_blueprint.add_url_rule(u'/<id>/delete', methods=[u'GET', u'POST'],view_func=delete)