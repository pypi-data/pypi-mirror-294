
This package is currently in beta. It is meant to render paralex lexicon files in mkdocs sites.

# Installing

```bash
pip install mkdocs_paralex_plugin
```

# Mkdocs 

Create a configuration file for [mkdocs](https://www.mkdocs.org/user-guide/), compatible with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/). 

It needs a special `paralex` section, with minimally a `paralex_package_path` (to the json file), lists of feature labels to use to separate tables, rows and columns. It can contain 

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

If your lexicon is massive, the generated site might exceed the free hosting capacity on gitlab or github. You can then add two more keys under the paralex section. If `sample_size` is set, the corresponding number of lexemes will be selected, and the site will only show that sample. If `frequency_sample` is set to `true`, then the chosen lexemes will be the most frequent.

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      sample_size: 5000
      frequency_sample: true
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

# Generating the site in a pipeline

To generate the site, add a pipeline file:

=== "gitlab pages"
    
    With gitlab, create a plain text file called `.gitlab-ci.yml`, with the following content. The site will then be served at `https://<username>.gitlab.io/<repository-name>`. For more on gitlab pages, see [the gitlab pages docs](https://docs.gitlab.com/ee/user/project/pages/). 

    ``` yaml title=".gitlab-ci.yml"
    image: python:3.8

    pages:
      stage: deploy
      script:
        - mkdir -p docs/
        - pip install pandas mkdocs>=1.1.2 mkdocs-material mkdocs_paralex_plugin
        - mkdocs build -d public/ --strict --verbose
      artifacts:
        paths:
          - public/
      only:
        - master
    ```
