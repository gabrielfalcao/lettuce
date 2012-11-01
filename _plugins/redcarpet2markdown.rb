require 'fileutils'
require 'digest/md5'
require 'redcarpet'
require 'pygments.rb'


class HTMLwithPygments < Redcarpet::Render::HTML
  def block_code(code, language)
    language = language || "console"
    Pygments.highlight(code, :lexer => language.to_sym, :options => {
      :encoding => 'utf-8'
    })
  end
end

def from_markdown(text)
  markdown = Redcarpet::Markdown.new(HTMLwithPygments,
    :fenced_code_blocks => true,
    :no_intra_emphasis => true,
    :autolink => true,
    :strikethrough => true,
    :lax_html_blocks => true,
    :superscript => true,
    :hard_wrap => false,
    :tables => true,
    :xhtml => false)

  text.gsub!(/\{\{( *)?"(.*?)"\}\}/, '\1\2')
  text.gsub!(/^\{% highlight (.+?) ?%\}(.*?)^\{% endhighlight %\}/m) do |match|
    Pygments.highlight($2, :lexer => $1, :options => {:encoding => 'utf-8'})
  end

  markdown.render(text)
end
class Jekyll::MarkdownConverter
  def extensions
    Hash[ *@config['redcarpet']['extensions'].map {|e| [e.to_sym, true] }.flatten ]
  end

  def markdown
    @markdown ||= Redcarpet::Markdown.new(Redcarpet2Markdown.new(extensions), extensions)
  end

  def convert(content)
    from_markdown(content)
  end
end
