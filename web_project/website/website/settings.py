"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h#ufun#x@)z)l@fe8yqjvm02m@gqyp#ln-xsr+!8e#s*46--_4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'crispy_forms',
    'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'ckeditor',
    'django_ckeditor_5',
    #'ckeditor_uploader',
    'taggit',
    'tinymce',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    #'default': {
      #  'ENGINE': 'django.db.backends.postgresql',
        #'NAME': 'James',
        #'USER': 'postgres',
        #'PASSWORD': '9054',
        #'HOST': 'localhost'

    #}
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#CKEDITOR_CONFIGS = {
 #   'default': {
  #      'height': '500',
   #     'width': 'auto',
      # 'toolbar': [["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
       #        ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
        #         'JustifyRight', 'JustifyBlock'],
         #       [ "Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], ['Undo', 'Redo'], ["Source"],
          #     ["Maximize"]],
       # 'toolbar':'full',
   # },
    #}
    #'default': {
    #'height': '500',
    #'width': 'auto',
   # 'skin': 'moono',
   # 'toolbar_Basic': [
    #    ['Source', '-', 'Bold', 'Italic']
    #],
    #'toolbar_YourCustomToolbarConfig': [

      #  {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},

      #  {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
      #  {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
        #{'name': 'forms',
       ##  'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
         #          'HiddenField']},
        #'/',
        #{'name': 'basicstyles',
        # 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
        #{'name': 'paragraph',
         #'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
          #         'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
        #           'Language']},
        
        #{'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
        #{'name': 'insert',
         #'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe', 'CodeSnippet']},
        #'/',
        #{'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        #{'name': 'colors', 'items': ['TextColor', 'BGColor']},
        #{'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
        #{'name': 'youtube', 'items': ['Youtube',]},
         # put this " '/', "  to force next toolbar on new line
        #{'name': 'yourcustomtools', 'items': [
            # put the name of your editor.ui.addButton here
         #   'media',
            #'Maximize',

        #]},


    #],


    #'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
    #'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],

    # 'height': 291,
    # 'width': '100%',
    # 'filebrowserWindowHeight': 725,
    # 'filebrowserWindowWidth': 940,
    # 'toolbarCanCollapse': True,
    # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
    #'tabSpaces': 4,
   #'extraPlugins': ','.join([
    #'image2',
    #'moonocolor',
      
      #'uploadimage', # the upload image feature
        # your extra plugins here
       # 'div',
        #'autolink',
        #'autoembed',
        #'embedsemantic',
        #'autogrow',
        # 'devtools',
        #'widget',
        #'lineutils',
        #'clipboard',
        #'dialog',
        #'dialogui',
        #'elementspath'
   #]),
    #'extraPlugins': 'image2,youtube',


#},
# my costum tool bar i created 


#}
#CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 


TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'file print preview powerpaste casechange importcss tinydrive searchreplace autolink autosave save directionality advcode visualblocks visualchars fullscreen  link template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker textpattern noneditable help formatpainter permanentpen pageembed charmap tinycomments mentions  linkchecker emoticons advtable',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',
    'mobile': {
          'plugins': 'file print preview powerpaste casechange importcss tinydrive searchreplace autolink autosave save directionality advcode visualblocks visualchars fullscreen  link  template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker textpattern noneditable help formatpainter pageembed charmap mentions quickbars linkchecker emoticons advtable'
          },
    'width': 'auto',
    
        
}

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]
   # CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                'bulletedList', 'numberedList', 'blockQuote','imageUpload', 
                ],
        #'extraPlugins':'EasyImage',
        #'toolbar':'full',
    },
    'extends': {

        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote', 'imageUpload'
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote','imageUpload',
                     '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed',
                    'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', 'imageTitle', '|', 'imageStyle:alignLeft', 'imageStyle:full',
                       'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
               'full',
                'side',
               'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },

        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
#STATICFILES_DIRS = [ # for tinymce
 #       "static/",
#]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
#CKEDITOR_RESTRICT_BY_USER = True
#CKEDITOR_BROWSE_SHOW_DIRS = True
#CKEDITOR_RESTRICT_BY_DATE = True


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
#CKEDITOR_UPLOAD_PATH = "uploads/"



LOGIN_REDIRECT_URL = 'blog-articles'
LOGIN_URL = 'login'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'brianoigo785@gmail.com'
EMAIL_HOST_PASSWORD = 'mpweizgklgysgsrq'
