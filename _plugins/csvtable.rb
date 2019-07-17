class CSVTable < Liquid::Tag
  def initialize(tagName, markup, tokens)
    super

    params = markup.split

    @csvdata = params.shift

    if params.size > 0
      @class = params.shift
    end
  end

  def render(context)
    csvdata = context[@csvdata]

    markup = ""
    if @class != nil
      markup += "<div class=\"csvtable #{@class}\"><table>"
    else
      markup += "<div class=\"csvtable\"><table>"
    end

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

    markup += "</table></div>"

    markup
  end

  Liquid::Template.register_tag "csvtable", self
end