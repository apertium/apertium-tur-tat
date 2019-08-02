Turkish and Tatar: `apertium-tur-tat`
===============================================================================

This is an Apertium language pair for translating between Turkish and
Tatar. What you can use this language package for:

* Translating between Turkish and Tatar
* Morphological analysis of Turkish and Tatar
* Part-of-speech tagging of Turkish and Tatar

For information on the latter two points, see subheading "For more
information" below.

Requirements
-------------------------------------------------------------------------------

You will need the following software installed:

* lttoolbox (>= 3.3.0)
* apertium (>= 3.3.0)
* vislcg3 (>= 0.9.9.10297)
* hfst (>= 3.8.2)
* apertium-tur
* apertium-tat
* apertium-recursive

If this does not make any sense, we recommend you look at: www.apertium.org.

Compiling
-------------------------------------------------------------------------------

Given the requirements being installed, you should be able to just run:

```console
$ ./configure
$ make
# make install
```

You can use `./autogen.sh` instead of `./configure` in case you're compiling
from source. If you installed any prerequisite language packages using a
`--prefix` with `./configure`, make sure to use the same `--prefix` when running
`./configure` here.

Testing
-------------------------------------------------------------------------------

If you are in the source directory after running make, the following
command should work:

```console
$ echo Авылларда кешеләр җыешкан һәр 1 сумга республика бюджетыннан 4 сум өстәлә. | apertium -d . tat-tur
Köylerde kişilerin topladığı her 1 rubleye cumhuriyet bütçesinden 4 ruble ekleniyor.
```

After installing somewhere in `$PATH`, you should be able to do e.g.

```console
$ echo Авылларда кешеләр җыешкан һәр 1 сумга республика бюджетыннан 4 сум өстәлә. | apertium tat-tur
Köylerde kişilerin topladığı her 1 rubleye cumhuriyet bütçesinden 4 ruble ekleniyor.
```

Files and data
-------------------------------------------------------------------------------

* [`apertium-tur-tat.tur-tat.dix`](apertium-tur-tat.tur-tat.dix) - Bilingual dictionary
* [`apertium-tur-tat.tur-tat.rtx`](apertium-tur-tat.tur-tat.rtx) - Recursive rules for translating into Tatar
* [`apertium-tur-tat.tat-tur.rtx`](apertium-tur-tat.tat-tur.rtx) - Recursive rules for translating into Turkish
* [`apertium-tur-tat.tur-tat.lrx`](apertium-tur-tat.tur-tat.lrx) - Lexical selection rules for translating into Tatar
* [`apertium-tur-tat.tat-tur.lrx`](apertium-tur-tat.tat-tur.lrx) - Lexical selection rules for translating into Turkish
* [`modes.xml`](modes.xml) - Translation modes

For more information
-------------------------------------------------------------------------------

* http://wiki.apertium.org/wiki/Installation
* http://wiki.apertium.org/wiki/apertium-tur-tat
* http://wiki.apertium.org/wiki/Using_an_lttoolbox_dictionary

Help and support
-------------------------------------------------------------------------------

If you need help using this language pair or data, you can contact:

* Mailing list: apertium-stuff@lists.sourceforge.net
* IRC: `#apertium` on irc.freenode.net (irc://irc.freenode.net/#apertium)

See also the file [`AUTHORS`](AUTHORS), included in this distribution.
