import django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models import CMSPlugin
from cms.models.fields import PageField
from filer.fields.image import FilerImageField
from django.conf import settings
from distutils.version import LooseVersion

from cmsplugin_filer_utils import FilerPluginManager

CMSPLUGIN_FILER_TEASER_STYLE_CHOICES = getattr( settings, 'CMSPLUGIN_FILER_TEASER_STYLE_CHOICES',() )

try:
    from settings import TEASER_PLUGIN_TEMPLATES
except:
   TEASER_PLUGIN_TEMPLATES = (
            ('slider.html', 'Slider'),
            ('list.html', 'List'),
            ('tabs.html', 'tabs'),
            ('fader.html', 'fader'),
            ('gallery-list.html', 'gallery List'),
            )



class FilerTeaser(CMSPlugin):
    """
    A Teaser
    """
    title = models.CharField(_("title"), max_length=255, blank=True)
    image = FilerImageField(blank=True, null=True, verbose_name=_("image"))
    if LooseVersion(django.get_version()) < LooseVersion('1.5'):
        image_url = models.URLField(_("alternative image url"), null=True, blank=True, default=None)
    else:
        image_url = models.URLField(_("alternative image url"), null=True, blank=True, default=None)
    
    style = models.CharField(_("teaser style"), max_length=255, null=True, blank=True, choices=CMSPLUGIN_FILER_TEASER_STYLE_CHOICES)
    
    use_autoscale = models.BooleanField(_("use automatic scaling"), default=True, 
                                        help_text=_('tries to auto scale the image based on the placeholder context'))
    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    
    free_link = models.CharField(_("link"), max_length=255, blank=True, null=True, help_text=_("if present image will be clickable"))
    page_link = PageField(null=True, blank=True, help_text=_("if present image will be clickable"), verbose_name=_("page link"))
    description = models.TextField(_("description"), blank=True, null=True)
    
    target_blank = models.BooleanField(_("open link in new window"), default=False)

    objects = FilerPluginManager(select_related=('image', 'page_link'))
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Make sure that either image or image_url is set
        if self.image and self.image_url:
            raise ValidationError(_('Either an image or an image url must be selected.'))
    
    def __unicode__(self):
        return self.title

    @property
    def link(self):
        try:
            if self.free_link:
                return self.free_link
            elif self.page_link and self.page_link:
                return self.page_link.get_absolute_url()
            else:
                return ''
        except Exception, e:
            print e

class FilerTeaserItem(models.Model):
    """
    A Teaser
    """
    title = models.CharField(_("title"), max_length=255, blank=True)
    image = FilerImageField(blank=True, null=True, verbose_name=_("image"))
    if LooseVersion(django.get_version()) < LooseVersion('1.5'):
        image_url = models.URLField(_("alternative image url"), null=True, blank=True, default=None)
    else:
        image_url = models.URLField(_("alternative image url"), null=True, blank=True, default=None)
    
    style = models.CharField(_("teaser style"), max_length=255, null=True, blank=True, choices=CMSPLUGIN_FILER_TEASER_STYLE_CHOICES)
    
    use_autoscale = models.BooleanField(_("use automatic scaling"), default=True, 
                                        help_text=_('tries to auto scale the image based on the placeholder context'))
    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    
    free_link = models.CharField(_("link"), max_length=255, blank=True, null=True, help_text=_("if present image will be clickable"))
    page_link = PageField(null=True, blank=True, help_text=_("if present image will be clickable"), verbose_name=_("page link"))
    description = models.TextField(_("description"), blank=True, null=True)
    
    target_blank = models.BooleanField(_("open link in new window"), default=False)

    objects = FilerPluginManager(select_related=('image', 'page_link'))
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Make sure that either image or image_url is set
        if self.image and self.image_url:
            raise ValidationError(_('Either an image or an image url must be selected.'))
    
    def __unicode__(self):
        return self.title

    @property
    def link(self):
        try:
            if self.free_link:
                return self.free_link
            elif self.page_link and self.page_link:
                return self.page_link.get_absolute_url()
            else:
                return ''
        except Exception, e:
            print e

#@python_2_unicode_compatible
class FilerTeaserList(CMSPlugin):

    name = models.CharField(max_length=128)
    description = models.TextField(_("description"), blank=True, null=True)
    filer_teasers = models.ManyToManyField("FilerTeaserItem",blank=True,null=True)
    template = models.CharField('Template', max_length=255,
                                            choices = TEASER_PLUGIN_TEMPLATES)

    def copy_relations(self, oldinstance):
            self.filer_teasers = oldinstance.filer_teasers.all()

    def __unicode__(self):
        return self.name
