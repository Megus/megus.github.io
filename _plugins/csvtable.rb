class CSVTable < Liquid::Tag
  def initialize(tagName, markup, tokens)
    super
    @csvdata = markup
  end

  def render(context)
    csvdata = context[@csvdata]
    markup = "<table>"

    # Header
    markup += "<tr>"
    csvdata[0].each_key do |h|
      markup += "<th>#{h}</th>"
    end
    markup += "</tr>"

    # Body
    csvdata.each do |row|
      markup += "<tr>"
      row.each_value do |v|
        markup += "<td>#{v}</td>"
      end

      markup += "</tr>"
    end

    markup += "</table>"

    markup
  end

  Liquid::Template.register_tag "csvtable", self
end