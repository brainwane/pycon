# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from markedit.widgets import MarkEdit

from symposion.proposals.kinds import register_proposal_form
from .models import (PyConProposalCategory, PyConTalkProposal,
                     PyConCharlaProposal, PyConTutorialProposal,
                     PyConPosterProposal, PyConLightningTalkProposal,
                     PyConSponsorTutorialProposal, PyConOpenSpaceProposal,
                     EduSummitTalkProposal, PyConProposal,
                     PyConStartupRowApplication)


def strip(text):
    return u' '.join(text.strip().split())


class PyConProposalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PyConProposalForm, self).__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
            queryset=PyConProposalCategory.objects.order_by("name")
        )


class PyConTalkProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConTalkProposalForm, self).__init__(*args, **kwargs)
        del self.fields["category"]

    def clean(self):
        # We no longer ask for an "audience level" for talk proposals,
        # but we still need to force it to a value that the database
        # will accept.
        cleaned_data = super(PyConTalkProposalForm, self).clean()
        cleaned_data['audience_level'] = (
            PyConTalkProposal.AUDIENCE_LEVEL_INTERMEDIATE)
        return cleaned_data

    class Meta:
        model = PyConTalkProposal
        fields = [
            "title",
            "duration",
            "description",
            "audience",
            "outline",
            "additional_notes",
            "recording_release",
            # Hidden fields:
            "audience_level",
        ]
        widgets = {
            "description": MarkEdit(),
            "audience_level": forms.HiddenInput(
                attrs={'value': PyConTalkProposal.AUDIENCE_LEVEL_INTERMEDIATE},
            ),
        }
        help_texts = {
            'title': strip(
                u"""
                Puns, jokes, or “hooks” in titles are okay,
                but make sure that if all someone knew was the title,
                they still would have some idea what the presentation is about.
                """
            ),
        }


register_proposal_form('talk', PyConTalkProposalForm)

class PyConCharlaProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConCharlaProposalForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = u'Título'
        self.fields['description'].label = u'Descripción corta'
        self.fields['outline'].label = u'Descripción'
        self.fields['additional_notes'].label = u'Notas sobre el ponente'
        self.fields['recording_release'].label = u'Liberación de la grabación'
        del self.fields["category"]

    def clean(self):
        # We no longer ask for an "audience level" for talk proposals,
        # but we still need to force it to a value that the database
        # will accept.
        cleaned_data = super(PyConCharlaProposalForm, self).clean()
        cleaned_data['audience_level'] = (
            PyConCharlaProposal.AUDIENCE_LEVEL_INTERMEDIATE)
        return cleaned_data

    class Meta:
        model = PyConCharlaProposal
        fields = [
            "title",
            "description",
            "outline",
            "additional_notes",
            "recording_release",
            # Hidden fields:
            "audience_level",
        ]
        widgets = {
            "description": MarkEdit(),
            "audience_level": forms.HiddenInput(
                attrs={'value': PyConTalkProposal.AUDIENCE_LEVEL_INTERMEDIATE},
            ),
        }
        help_texts = {
            'title': strip(u""),
            'description': strip(u"Resumen de qué trata la charla y por qué es interesante para los asistentes."),
            'outline': strip(u"Cual es el tema de la charla, que va a cubrir y por qué esta charla deberia ser elegida para las PyCon Charlas."),
            'additional_notes': strip(u"Informacion general sobre el ponente para los revisores. Experiencia previa, dominio del tema, etc."),
            'recording_release': strip(u"Al enviar tu propuesta estás de acuerdo con dar permiso a la Python Software Foundation de grabar, editar y liberar el audio y/o vídeo de tu presentación. Si no estás de acuerdo, por favor desmarca la casilla. Dirígete a <a href=\"/2019/speaking/recording/\">liberación de grabaciones PyCon 2019</a> para más detalles."),
        }


register_proposal_form('charla', PyConCharlaProposalForm)


class PyConLightningTalkProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConLightningTalkProposalForm, self).__init__(*args, **kwargs)
        self.fields['audience_level'].widget = forms.HiddenInput()
        self.fields['audience_level'].initial = PyConLightningTalkProposal.AUDIENCE_LEVEL_NOVICE

    class Meta:
        model = PyConLightningTalkProposal
        fields = [
            "title",
            "category",
            "description",
            "additional_notes",
            "additional_requirements",
            "audience_level",
            "recording_release",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }


register_proposal_form('lightning-talk', PyConLightningTalkProposalForm)


class PyConTutorialProposalForm(PyConProposalForm):
    def __init__(self, *args, **kwargs):
        super(PyConTutorialProposalForm, self).__init__(*args, **kwargs)
        del self.fields["category"]

    class Meta:
        model = PyConTutorialProposal
        fields = [
            "title",
            "audience_level",
            "domain_level",
            "description",
            "audience",
            "outline",
            "additional_notes",
            "recording_release",
        ]
        widgets = {
             "audience_level": forms.HiddenInput(
                 attrs={'value':
                        PyConTutorialProposal.AUDIENCE_LEVEL_INTERMEDIATE},
             ),
             "domain_level": forms.HiddenInput(
                 attrs={'value':
                        PyConTutorialProposal.DOMAIN_LEVEL_INTERMEDIATE},
             ),
            "description": MarkEdit(),
            "perceived_value": forms.Textarea(attrs={'rows': '3'}),
        }
        help_texts = {
            'additional_notes': strip(
                u"""
                (a) If you have offered this tutorial before,
                please provide links to the material and video, if possible.
                Otherwise, please provide links to one (or two!)
                previous presentations by each speaker.
                (b) Please summarize your teaching
                or public speaking experience
                and your experience with the subject of the tutorial.
                (c) Let us know if you have specific needs or special requests —
                for example, requests that involve accessibility, audio,
                or restrictions on when your talk can be scheduled.
                """
            ),
            'outline': strip(
                u"""
                Make an outline that lists the topics and activities
                you will guide your students through
                over the 3 hours of your tutorial.
                Provide timings for each activity —
                indicate when and for how long you will lecture,
                and when and for how long students
                will be tackling hands-on exercises.
                This is a very important criteria!
                Generally speaking, the more detailed the outline,
                the more confidence the committee will have
                that you can deliver the material in the allotted time.
                """
            ),
        }


register_proposal_form('tutorial', PyConTutorialProposalForm)


class PyConPosterProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConPosterProposalForm, self).__init__(*args, **kwargs)
        del self.fields["category"]

    class Meta:
        model = PyConPosterProposal
        fields = [
            "title",
            "audience_level",
            "description",
            "additional_notes",
            "additional_requirements",
        ]
        widgets = {
            "audience_level": forms.HiddenInput(
                attrs={'value':
                       PyConTutorialProposal.AUDIENCE_LEVEL_INTERMEDIATE},
            ),
            "description": MarkEdit(),
        }
        help_texts = {
            'additional_notes': strip(u"""
            Additional notes for the program committee, like:<br>
            Have you presented on this poster’s topic before?<br>
            What are your qualifications and experiences in this area?<br>
            Links to any related publications, slides, or source code.<br>
            Will you need electrical power?<br>
            Do you have accessibility needs that we should plan ahead for?
            """),
            'additional_requirements': strip(u'''
            Please let us know if you have any requirements for presenting your
            poster such as a 6 foot table for a demo.
            '''),
        }


register_proposal_form('poster', PyConPosterProposalForm)


class PyConOpenSpaceProposalForm(PyConProposalForm):

    class Meta:
        model = PyConOpenSpaceProposal
        fields = [
            "title",
            "description",
            "additional_notes",
            "additional_requirements",
            "audience_level",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(PyConProposalForm, self).__init__(*args, **kwargs)
        self.fields['audience_level'].widget = forms.HiddenInput()
        self.fields['audience_level'].initial = PyConLightningTalkProposal.AUDIENCE_LEVEL_NOVICE

    def clean_description(self):
        value = self.cleaned_data["description"]
        return value


register_proposal_form('open-space', PyConOpenSpaceProposalForm)


class PyConSponsorTutorialForm(PyConProposalForm):

    class Meta:
        model = PyConSponsorTutorialProposal
        fields = [
            "title",
            "description",
            "abstract",
            "additional_notes",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
        }


register_proposal_form('sponsor-tutorial', PyConSponsorTutorialForm)


class EducationSummitTalkProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(EducationSummitTalkProposalForm, self).__init__(*args, **kwargs)
        self.fields['audience_level'].widget = forms.HiddenInput()
        self.fields['audience_level'].initial = PyConProposal.AUDIENCE_LEVEL_NOVICE
        del self.fields["category"]

    class Meta:
        model = EduSummitTalkProposal
        fields = [
            "title",
            "description",
            "additional_notes",
            "audience_level",
            "recording_release",
        ]
        widgets = {
            "description": MarkEdit(),
        }


register_proposal_form('edusummit', EducationSummitTalkProposalForm)


class PyConStartupRowApplicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(PyConStartupRowApplicationForm, self).__init__(*args, **kwargs)
        self.fields["applicant_name"].label = u'Your name'
        self.fields["applicant_company_role"].label = u'Your role at your company'
        self.fields["company_name"].label = u'Company name'
        self.fields["company_url"].label = u'Company URL'
        self.fields["company_location"].label = u'Where is your company based?'
        self.fields["company_activity"].label = u'What does your company do?'
        self.fields["company_python_usage"].label = u'How is Python used at your company?'
        self.fields["company_age"].label = u'How long has your company been active?'
        self.fields["company_size"].label = u'How many full-time employees, including founders, work at your company?'
        self.fields["company_competitive_advantage"].label = u'What is your competitive advantage?'
        self.fields["company_monetization_strategy"].label = u'How will your company make money?'
        self.fields["company_funding"].label = u'How has your company funded its development and growth?'
        self.fields["company_additional_notes"].label = u'Anything else you\'d like to tell us?'
        self.fields["company_demo_url"].label = u'Product demo/video URL?'

    class Meta:
        model = PyConStartupRowApplication
        fields = [
            "applicant_name",
            "applicant_company_role",
            "company_name",
            "company_url",
            "company_location",
            "company_activity",
            "company_python_usage",
            "company_age",
            "company_size",
            "company_competitive_advantage",
            "company_monetization_strategy",
            "company_funding",
            "company_additional_notes",
            "company_demo_url",
        ]
        widgets = {
        }
        help_texts = {
            "applicant_name": None,
            "applicant_company_role": None,
            "company_name": None,
            "company_url": "Optional",
            "company_location": None,
            "company_activity": "500 Characters or less",
            "company_python_usage": "500 Characters or less",
            "company_age": None,
            "company_size": None,
            "company_competitive_advantage": "500 Characters or less",
            "company_monetization_strategy": "500 Characters or less",
            "company_funding": "Optional",
            "company_additional_notes": "Optional",
            "company_demo_url": "Optional",
        }

    def save(self, commit=True):
        obj = super(PyConStartupRowApplicationForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj
