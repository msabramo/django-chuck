# -*- coding: utf-8 -*-
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from tellafriend.forms import TellAFriendForm

def tellafriend(request):
    """Displays the tell-a-friend form and sends out the e-mail"""

    current_site = Site.objects.get_current()
    domain = current_site.domain

    full_url = 'http://www.%s' % domain

    if request.method == 'POST':
        form = TellAFriendForm(request.POST)

        if form.is_valid():

            # recommend mail
            email_context = request.POST.copy()
            email_context.update({
                'full_url': full_url,
            })

            text_content = render_to_string('tellafriend/email.txt', email_context, context_instance=RequestContext(request))
            msg = EmailMultiAlternatives(request.POST.get('email_sender') + " " + _(u"wünscht dir Merry KissMas!"),
                                         text_content,
                                         request.POST.get('email_sender'),
                                         [request.POST.get('email_recipient')])
            msg.send()

            return HttpResponseRedirect(reverse('tellafriend_success'))
    else:
        
        if request.LANGUAGE_CODE == 'de':
            initial_message = u'Hallo \n\nFür jeden Weihnachtskuss auf der Website www.kissmas.ch spendet Swisscom 1 Franken an «Jeder Rappen zählt», die Aktion von Schweizer Radio und Fernsehen und der Glückskette für Mütter in Not.\n\nMeinen Weihnachtskuss findets du bereits auf der KissMas Wall. Mach doch auch mit - es ist so einfach, mit einem Kuss sich und anderen etwas Gutes zu tun.\n\nMerry KissMas!'
        else:
            initial_message = u'Hello\n\nPour chaque baiser de Noël téléversé sur www.kissmas.ch, Swisscom  verse 1 franc à «Jeder Rappen zählt» , la collecte des radios et télévisions suisses alémaniques et de la Chaîne du Bonheur.\n\n Tu trouveras mon baiser de Noël sur le mur KissMass. Envoie aussi ton baiser – c’est si simple de se faire plaisir et de faire plaisir aux autres.\n\n Merry KissMas!'

        form = TellAFriendForm(initial={'message': initial_message})

    return render_to_response('tellafriend/tellafriend.html', {'tellafriend_form': form, 'tellafriend_full_url': full_url}, context_instance=RequestContext(request))