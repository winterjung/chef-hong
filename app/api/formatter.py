from jinja2 import Template


class DefaultFormatter:
    template = (  # noqa
        '{{ date }} {{ weekday }}\n\n' +
        '{% for place in places %}' +
        '□ {{ place["name"] }}\n' +
            '{% for time in place["time"] %}' +
                '■ {{ time["name"] }}\n' +
                '{{ time["text"] }}\n' +
            '{% endfor %}\n' +
        '{% endfor %}'
    )

    @classmethod
    def format(cls, **kwargs):
        places = kwargs.pop('places')
        date = kwargs.pop('date')
        weekday = kwargs.pop('weekday')

        return Template(cls.template).render(
            date=date,
            weekday=weekday,
            places=places
        )
