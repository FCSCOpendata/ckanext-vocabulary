import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.vocabulary.blueprints.vocabulary import vocab_blueprint

class VocabularyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'vocabulary')

    
    # IBlueprint
    def get_blueprint(self):
        return [ vocab_blueprint ]

