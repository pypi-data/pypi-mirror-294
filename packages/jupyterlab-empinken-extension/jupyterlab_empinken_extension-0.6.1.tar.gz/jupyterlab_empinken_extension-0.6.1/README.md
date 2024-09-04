# jupyterlab_empinken_extension

A JupyterLab extension for colouring notebook cell backgrounds.

Builds on [`jupyterlab-celltagsclasses`](https://github.com/parmentelat/jupyterlab-celltagsclasses) and earlier versions of `jupyterlab_empinken_extension`.

![empinken backgrounds](images/empinken-backgrounds.png)

![empinken settings](images/empinken-settings.png)

The buttons set tags on selected cells and the cell is styled correspondingly.

In v0.6.x:

![New empinken MDI icons - book-open-outline, check, school-outline, format-quote-close](images/empinken-new-icons.png)

- [*book* / `book-open-outline` icon](https://pictogrammers.com/library/mdi/icon/book-open-outline/): "activity" [maps to `style-activity` cell tag], by default, a blue background; used to idnetify activity blockls (follows OU VLE theme);
- [*tick* / `check` icon](https://pictogrammers.com/library/mdi/icon/check/): "solution" [maps to `style-solution` cell tag], by default, a green background; used to identify solution cells;
- [*head/mortarboard* ("scholar") / `school-outline` icon](https://pictogrammers.com/library/mdi/icon/school-outline/): "learner" [maps to cell tag `style-learner`], by default, a yellow background; used as a nudge to students ("you should edit / add content to this cell");
- [*quote* / `format-quote-close` icon](https://pictogrammers.com/library/mdi/icon/format-quote-close/): "tutor" [maps to cell tag `style-tutor`], by default, a pink background; used by tutors to highlight feedback cells; used by editors/critical readers to highlight feedback cells to authors.

*Icons from [Material Design Icons](https://pictogrammers.com/library/mdi/)*

In `0.5.5`:

- `A`: "activity" [maps to `style-activity` cell tag], by default, a blue background; used to idnetify activity blockls (follows OU VLE theme);
- `S`: "solution" [maps to `style-solution` cell tag], by default, a green background; used to identify solution cells;
- `L`: "learner" [maps to cell tag `style-learner`], by default, a yellow background; used as a nudge to students ("you should edit / add content to this cell");
- `T`: "tutor" [maps to cell tag `style-tutor`], by default, a pink background; used by tutors to highlight feedback cells; used by editors/critical readers to highlight feedback cells to authors.

Associated tools: in [`tm351_nb_utils`](https://github.com/innovationOUtside/nb_workflow_tools) command lines tools:

- [empinken tags updater](https://github.com/innovationOUtside/nb_workflow_tools/tree/master?tab=readme-ov-file#empinken-updater) (to `style-activity`/`style-solution`/`style-learner`/`style-tutor` format): `upgrade_empinken_tags NOTEBOOKS_PATH`
- 
## Requirements

- JupyterLab >= 4.0.0

## Initial set-up

```bash
# Create orphan branch
% git checkout --orphan NEWBRANCH

# Clear old files
git rm -rf .

# Use template to create base extenion
copier copy https://github.com/jupyterlab/extension-template .

```

## Install

To install the extension, execute:

```bash
pip install jupyterlab_empinken_extension
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyterlab_empinken_extension
```

## TH BUILD

`jlpm build`

`hatch build`

## Contributing

### Set up environment

`cd` into dir and run `pipenv install`

Each terminal session, `cd` into dir and run `pipenv shell`.

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the jupyterlab_empinken_extension directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes

```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall jupyterlab_empinken_extension
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `jupyterlab_empinken_extension` within that folder.

### Testing the extension

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
