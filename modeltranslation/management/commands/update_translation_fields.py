
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand

from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname

class Command(BaseCommand):
    help = 'Updates the default translation fields of all or the specified'\
           'application using the value of the original field.'
    args = '[app_name]'
        
    def handle(self, subscriber_list_slug, **options):        
        default_lang = settings.LANGUAGES[0][0]        
        if 'settings' in options and options['settings']:
            custom_settings = options['settings']
            # print "Got custom settings:", custom_settings
            default_lang = custom_settings.LANGUAGES[0][0]

        # print "default lang:", default_lang
        
        for model, trans_opts in translator._registry.items():
            print model, trans_opts
            # Get all the instances of the model
            for obj in model.objects.all():
                print obj
                for fieldname in trans_opts.fields:
                    def_lang_fieldname = build_localized_fieldname(fieldname, default_lang)
                    print "setting %s from %s to %s." % (def_lang_fieldname, fieldname, obj.__dict__[fieldname])
                    if not getattr(obj, def_lang_fieldname):
                        setattr(obj, def_lang_fieldname, obj.__dict__[fieldname])
                obj.save()