from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectMultipleField,
    DateTimeField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    ValidationError
)

options = [
    ('OptionA', 'OptionA'),
    ('OptionB', 'OptionB'),
]

def validate_option(form, option):
    options = [
        'OptionA',
        'OptionB'
    ]
    for option in option.data:
        if option not in options:
            raise ValidationError(
                'This option is not allowed'
            )


class ItemForm(FlaskForm):
    typealist_id = StringField(
        'typealist_id'
    )
    typeblist_id = StringField(
        'typeblist_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )
    submit = SubmitField("Create Item")


class TypeBListForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    submit = SubmitField("Create a TypeBList")


class TypeBListEditForm(TypeBListForm):
    submit = SubmitField("Edit TypeBList")


class TypeAListForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    options = SelectMultipleField(
        'options', validators=[DataRequired(), validate_option],
        choices=options
     )
    submit = SubmitField("Create TypeAList")


class TypeAListEditForm(TypeAListForm):
    submit = SubmitField("Edit TypeAList")
