FROM ruby:3.3

RUN apt-get update && apt-get install -y build-essential nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN gem install bundler:2.5.17 && bundle install --jobs 4

CMD ["bundle", "exec", "jekyll", "serve", "-H", "0.0.0.0", "--livereload", "--force_polling"]
