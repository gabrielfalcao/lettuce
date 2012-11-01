module TextFilter
  def slug(input)
    input.downcase.gsub(/\W+/, '-')
  end
end

Liquid::Template.register_filter(TextFilter)
