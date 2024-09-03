# Snowdrop

A fork of [mistletoe](https://github.com/miyuchina/mistletoe).

This fork adds classes automatically to the `<p>` tags that are generated that
wrap blocks of text.

It does this by combining the lowercase of the first three words with dashes.
So, for example, the class for this paragraph would be 'it-does-this'.

## Installation

    pip install snowdrop

## Usage

    import snowdrop

    html = snowdrop.markdown(markdown)
