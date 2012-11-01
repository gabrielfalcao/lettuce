server: prepare
	@printf "\033[1;32mjekyll --url http://localhost:4000\033[0m\n"
	@jekyll --url http://localhost:4000

prepare:
	@printf "\033[1;31mCleaning up current site...\033[0m"
	@rm -rf _site/*
	@printf "\033[1;31mOK\033[0m\n"


deploy: prepare
	@printf "\033[1;32mjekyll --no-server --no-auto\033[0m\n"
	@jekyll --no-server --no-auto

quick: deploy
