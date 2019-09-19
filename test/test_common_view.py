from mlstocks.common import view


class TestCommonView():


  def test_print_title(self, capsys):
    view.print_title('Title')
    assert 'Title\n=====\n\n' == capsys.readouterr().out


  def test_print_subtitle(self, capsys):
    view.print_subtitle('SubTitle')
    assert 'SubTitle\n--------\n\n' == capsys.readouterr().out


  # def test_print_entity(self, capsys):
  #   ent = v20.base_entity.BaseEntity()
  #   ent.attribute = 'value'
  #   ent._properties.append(Property(
  #     'attribute',
  #     'attribute',
  #     'attribute',
  #     'str',
  #     'str',
  #     False,
  #     ''
  #   ))
  #   ent.array = ['value']
  #   ent._properties.append(Property(
  #     'array',
  #     'array',
  #     'array',
  #     'array',
  #     'array',
  #     False,
  #     []
  #   ))
  #   ent.object = {}
  #   ent._properties.append(Property(
  #     'object',
  #     'object',
  #     'object',
  #     'object',
  #     'object',
  #     False,
  #     []
  #   ))
  #   view.print_entity(ent, 'BaseEntity')
  #   out = capsys.readouterr().out
  #   assert 'BaseEntity\n==========\n\n=========  ========\nattribute  value\narray      [1]\nobject     <object>\n=========  ========\n' == out

# if __name__ == '__main__':
