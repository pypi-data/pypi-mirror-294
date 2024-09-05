"""
Translatable version of edx-platform/xmodule.capa_block
"""

# pylint:  disable=unnecessary-lambda-assignment

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from xblock.fields import Scope
from xmodule.capa_block import ProblemBlock as BaseProblemBlock

from translatable_xblocks.base import TranslatableXBlock
from translatable_xblocks.fields import TranslatableString, TranslatableXMLString

# Make '_' a no-op so we can scrape strings. Using lambda instead of
#  `django.utils.translation.gettext_noop` because Django cannot be imported in this file
_ = lambda text: text


try:
    FEATURES = getattr(settings, "FEATURES", {})
except ImproperlyConfigured:
    FEATURES = {}


class ProblemBlock(TranslatableXBlock, BaseProblemBlock):
    """Our version of the ProblemBlock with added translation logic."""

    display_name = TranslatableString(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        # it'd be nice to have a useful default but it screws up other things; so,
        # use display_name_with_default for those
        default=_("Blank Problem"),
    )

    data = TranslatableXMLString(
        help=_("XML data for the problem"),
        scope=Scope.content,
        enforce_type=FEATURES.get("ENABLE_XBLOCK_XML_VALIDATION", True),
        default="<problem></problem>",
    )
