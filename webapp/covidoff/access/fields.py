from django.db.models.fields import CharField
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from random import SystemRandom
import string

def generate_cryptsafe_code(n, alpha):
    " Geneate a n digit cryptographically secure ID with given alphabet "
    cryptogen = SystemRandom()
    return "".join([str(alpha[cryptogen.randrange(len(alpha))]) for i in range(n)])

@deconstructible
class GenerateID(object):
    
    def __init__(self, length, alphabet=None):
        self.length = length
        self.alphabet = alphabet or string.digits + string.letters
        
    def __call__(self):
        return generate_cryptsafe_code(self.length, self.alphabet)

class SafeRandomField(CharField):
    
    default_validators = []
    description = _('Cryptographically secure random string')
    
    def __init__(self, *args, **kwargs):
        
        # Attributes are not yet checked or present in the class instance, so we need to
        # get max_length for the kwargs dictionary directly. This is not optimal. If max_length
        # is not defined by the caller this will default to 15 and django will throw an
        # exception when we call super.
        max_length = kwargs.get('max_length', 15)
        self.alphabet = kwargs.pop('alphabet', string.digits + string.ascii_letters)
        
        kwargs['default'] = kwargs.get('default', GenerateID(max_length, self.alphabet))
        
        super(SafeRandomField, self).__init__(*args, **kwargs)
        
    def check(self, **kwargs):
        errors = super(SafeRandomField, self).check(**kwargs)
        errors.extend(self._check_alphabet_attribute(**kwargs))
        return errors
    
    def _check_alphabet_attribute(self, **kwargs):
        
        if not isinstance(self.alphabet, str):
            return [
                checks.Error(
                    _("The 'alphabet' attribute must be a string"),
                    hint=None,
                    obj=self,
                    id='covidoff.E001'
                )
            ]
        
        return []
        