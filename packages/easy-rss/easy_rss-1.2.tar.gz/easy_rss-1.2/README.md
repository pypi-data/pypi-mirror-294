[![Generic badge](https://img.shields.io/badge/Licence-MIT-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-yes-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/easy_rss-1.2-red.svg)](https://pypi.org/project/easy-rss)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/easy_rss)](https://pypi.org/project/easy-rss)

# easy_rss
Simple Python package for processing data from RSS feeds

Can parse both `Atom` and `RSS` formats

### Usage
```python
from easy_rss import *

rss = EasyRSS("https://rss.nytimes.com/services/xml/rss/nyt/World.xml")
for item in rss.get_news():
    print(f"\n{item}\n")

```

### Output
```
Item(title='Live Updates: Russia Unleashes New Strikes as Ukraine Prepares for Cabinet Shake-Up', link='https://www.nytimes.com/live/2024/09/04/world/ukraine-russia-missile-attacks', pubDate='Sep 04, 2024 01:30PM', description='Several ministers offered to resign as President Volodymyr Zelensky laid plans for a major reshuffle of Ukraine’s government. While rescuers searched the rubble of a deadly strike on a military academy in eastern Ukraine, another Russian attack killed seven in the west.')


Item(title='Poltava Strike Aftermath Drains Ukraine’s Seasoned Rescuers', link='https://www.nytimes.com/2024/09/04/world/europe/ukraine-poltava-strike-aftermath.html', pubDate='Sep 04, 2024 05:50AM', description='Repeated air-raid alerts have punctuated the search through the rubble in Poltava, in eastern Ukraine, after an attack that killed more than 50 people.')


Item(title='With New Taliban Manifesto, Afghan Women Fear the Worst', link='https://www.nytimes.com/2024/09/04/world/asia/women-taliban-prohibitions-afghanistan.html', pubDate='Sep 04, 2024 12:37PM', description='Three years into its rule, the movement has codified its harsh Islamic decrees into law that now includes a ban on women’s voices in public.')


Item(title='Cease-Fire Talks Present Tough Choices for Gazans Devastated by War', link='https://www.nytimes.com/2024/09/04/world/middleeast/gaza-war-cease-fire-israel.html', pubDate='Sep 04, 2024 05:04AM', description='Some say they will reluctantly stomach a postwar Israeli military presence in the territory if that allows them to go home. Others worry about another long-term occupation.')
```
