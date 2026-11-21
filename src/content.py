# -*- coding: utf-8 -*-
# Site copy, v2: short, personal, notes-style.

def a(url, text):
    return f'<a href="{url}">{text}</a>'

def wiki(page, text):
    return a('https://en.wikipedia.org/wiki/' + page, text)

LAURELIN = a('https://laurelin.bio', 'Laurelin.bio')

def notes(*items):
    return '<ol class="notes">' + ''.join(f'<li>{t}</li>' for t in items) + '</ol>'

def img(key, caption):
    # replaced at build time with the embedded image and its credit
    return f'{{IMG:{key}|{caption}}}'

ABOUT_PARAS = [
    ('lead', 'Hi, I&rsquo;m Mahean. I originally hail from the Global South and grew up on a farm where the internet didn&rsquo;t really reach until late 2020.'),
    ('', 'I recently founded ' + a('https://foresightmachines.com', 'Foresight Machines') + '.'),
    ('', 'I study computational sciences at ' + a('https://www.minerva.edu', 'Minerva University') + ', which is backed by ' +
         a('https://www.benchmark.com', 'Benchmark') + ', and live in a different country each semester. '
         'When I&rsquo;m not abroad, I live in the great city of San Francisco.'),
    ('', 'Most recently, I spent a year on the core investment team at ' + a('https://m13.co', 'M13') +
         ', focused on AI and energy startups and building software for automation.'),
    ('', 'Some of my primal instincts are engineering foresight, engineering light in all its forms, and wondering at how much of space is still out there for us.'),
]

INTERESTS = []

# 01 simulation -------------------------------------------------------------
INTERESTS.append(('simulation', 'Simulation', [
    'I got into it through the simulation hypothesis, mostly via Rizwan Virk&rsquo;s book <i>The Simulation Hypothesis</i>, which connects it to science, religion and Eastern mysticism.',
    'These days I mostly think about simulating whole populations and the systems they live in, from a single company to a city to an entire economy. '
    + a('https://foresightmachines.com', 'Foresight Machines') + ' is my attempt at it. I think it has only just become possible.',
], notes(
    wiki('Simulation_hypothesis', 'Bostrom&rsquo;s 2003 argument') + ' is still the cleanest version: if civilisations run detailed simulations of their ancestors, simulated minds will vastly outnumber real ones.',
    'Musk, 2016: the odds we live in base reality are &ldquo;one in billions.&rdquo;',
    'Rizwan Virk, <i>The Simulation Hypothesis</i> (2019), and its sequel <i>The Simulated Multiverse</i> (2021). Virk is a video game designer and reads the idea through games: a game renders only what the player is looking at.',
    'Hindu and Buddhist traditions have an old word for something close: maya, the world as illusion.',
    'The useful version is older than computers. Ulam and von Neumann came up with the ' + wiki('Monte_Carlo_method', 'Monte Carlo method') + ' at Los Alamos in the 1940s: answer hard questions by playing out thousands of random cases.',
    wiki('Conway%27s_Game_of_Life', 'Conway&rsquo;s Game of Life') + ' (1970). Four rules on a grid, and you get gliders, guns that fire gliders, and eventually a universal computer.',
) + img('glider', 'Gosper&rsquo;s glider gun, the first known pattern in the Game of Life that grows forever.') + notes(
    'Schelling, 1971, with coins on a checkerboard: people who only mildly prefer neighbours like themselves still end up in a segregated city. The model is running below. Click to reseed.',
) + '''<figure class="fig" data-widget="schelling"><canvas aria-label="Schelling segregation model, running live"></canvas><span class="readout">tick 000</span></figure>''' + notes(
    wiki('The_Limits_to_Growth', '<i>The Limits to Growth</i>') + ' (1972) was the first serious attempt to simulate the whole world economy.',
    a('https://arxiv.org/abs/2304.03442', 'Park et al., 2023') + ': 25 language-model agents in a small town organised a Valentine&rsquo;s Day party nobody scripted.',
    a('https://arxiv.org/abs/2411.10109', 'Park et al., 2024') + ': agents built from interviews with about a thousand real people reproduced their survey answers 85% as well as the people themselves did two weeks later.',
    'Asimov called it ' + wiki('Psychohistory_(fictional)', 'psychohistory') + ': predicting the behaviour of large populations while individuals stay unpredictable. <i>Foundation</i>, 1951.',
    'A novel about being simulated: Greg Egan, ' + wiki('Permutation_City', '<i>Permutation City</i>') + '.',
)))

# 02 superforecasting -------------------------------------------------------
INTERESTS.append(('superforecasting', 'Superforecasting', [
    'I&rsquo;ve competed in forecasting tournaments and hosted them.',
    'This summer, AI forecasters matched the best human superforecasters for the first time. With more compute, better data and architectures built for the job, they&rsquo;ll keep improving. '
    'A simulation is only as good as the forecasts you feed it.',
], notes(
    '1950. Glenn Brier, a meteorologist, proposes scoring probability forecasts by squared error. The ' + wiki('Brier_score', 'Brier score') + ' still grades most tournaments.',
    '1950s. At RAND, Olaf Helmer and Norman Dalkey develop the ' + wiki('Delphi_method', 'Delphi method') + ': anonymous estimates, shared feedback, repeated rounds.',
) + img('rand', 'The RAND Corporation in Santa Monica. Delphi, scenario planning and much of early forecasting started at RAND.') + notes(
    '1960s. Herman Kahn, also at RAND, pushes scenarios over single predictions. Shell later uses them to get ready for the 1973 oil shock before its competitors.',
    '1988. The ' + wiki('Iowa_Electronic_Markets', 'Iowa Electronic Markets') + ' start trading on elections and often beat the polls.',
    '2003. DARPA&rsquo;s ' + wiki('Policy_Analysis_Market', 'Policy Analysis Market') + ' is cancelled within days of being announced.',
    '2005. Tetlock&rsquo;s ' + wiki('Philip_E._Tetlock', '<i>Expert Political Judgment</i>') + ': 284 experts, tens of thousands of predictions. On average they did little better than chance, though a few did much better.',
    '2011&ndash;15. IARPA funds a forecasting tournament. Tetlock and Mellers&rsquo;s ' + wiki('The_Good_Judgment_Project', 'Good Judgment Project') + ' wins, and its top volunteers get a name: superforecasters.',
    '2015. ' + wiki('Superforecasting:_The_Art_and_Science_of_Prediction', '<i>Superforecasting</i>') + ' comes out. ' + a('https://www.metaculus.com', 'Metaculus') + ' launches.',
    '2020s. Polymarket and Kalshi make prediction markets mainstream. The ' + a('https://forecastingresearch.org', 'Forecasting Research Institute') + ' runs tournaments on long-range questions.',
    '2024. ' + a('https://www.forecastbench.org', 'ForecastBench') + ' and Metaculus start scoring models against humans on questions that haven&rsquo;t resolved yet, so nothing can leak from training data.',
    '2026. Parity.',
    'Scott Alexander on ' + a('https://www.astralcodexten.com/archive?sort=search&search=superforecasters', 'Astral Codex Ten on AI superforecasters') + ', and his Mantic Monday posts on prediction markets.',
    'From hosting: a good question resolves cleanly, matters to someone, and stays uncertain for a while.',
    'Forecasting is easy to train on, since every question eventually resolves and gives a score.',
)))

# 03 augmented reality ------------------------------------------------------
INTERESTS.append(('augmented-reality', 'Augmented reality', [
    'My first software project, ' + a('https://devpost.com/software/oasis-labs', 'Oasis Labs') + ', tried to build a spatial layer on top of physical reality. The bet was that the platform after the smartphone would be the world itself, with its own social life and commerce.',
    'Later I studied metamaterials, because glasses you wear every day need much thinner lenses. The closest thing I&rsquo;ve seen to what I was trying to build is the Big Market in <i>Valerian and the City of a Thousand Planets</i>: a whole bazaar you can only see with a headset, sitting on top of an empty desert. I&rsquo;m very optimistic.',
], notes(
    a('https://devpost.com/software/oasis-labs', 'Oasis Labs') + ': digital objects anchored to real places, visible to anyone with the right device, and still there when you come back.',
    'Pok&eacute;mon Go (2016) showed the demand: millions of people walked around their cities to find creatures that only existed on their screens.',
    'The bottleneck is optics. Ordinary lenses bend light with thick curved glass, which is too heavy for glasses you&rsquo;d wear all day.',
    wiki('Metalens', 'Metalenses') + ' focus light with a flat layer of nanopillars, each shaped to delay light by a precise amount. Capasso&rsquo;s group at Harvard made them work across visible light in 2016.',
) + img('metalens', 'A metalens under an electron microscope. Each dot is a nanostructure; together they act as a lens.') + notes(
    'Ivan Sutherland built the first head-mounted display in 1968. It was so heavy it hung from the ceiling, so it was nicknamed ' + wiki('The_Sword_of_Damocles_(virtual_reality)', 'the Sword of Damocles') + '.',
    wiki('Valerian_and_the_City_of_a_Thousand_Planets', '<i>Valerian</i>') + ' (2017): tourists stand in an empty desert, put on a headset and gloves, and walk into the Big Market, a bazaar of thousands of stalls in another dimension. Without the gear, it&rsquo;s just sand.',
    'The film is based on ' + wiki('Val%C3%A9rian_and_Laureline', '<i>Val&eacute;rian and Laureline</i>') + ', the French comic by Christin and M&eacute;zi&egrave;res.',
    'Also: Vernor Vinge, <i>Rainbows End</i>. Keiichi Matsuda, <i>Hyper-Reality</i> (short film, 2016). Matthew Ball, <i>The Metaverse</i>.',
)))

# 04 capital ----------------------------------------------------------------
INTERESTS.append(('capital', 'Capital', [
    'Which ideas get funded decides which futures get built.',
    'A year deploying venture capital at ' + a('https://m13.co', 'M13') + ' left me thinking the biggest problems are time and speed: too little money for things that take a decade to prove, and too much process for small bets.',
], notes(
    'Venture returns follow a power law. In most funds one company returns more than all the others combined. ' + a('https://reactionwheel.net', 'Jerry Neumann') + ' has written the most careful work on this.',
    'Fund structure shapes what gets built. A ten-year fund wants an exit within ten years. Fusion, new materials and most of biology take longer.',
    a('https://fastgrants.org', 'Fast Grants') + ' (2020) made COVID research grants within 48 hours.',
    wiki('Science,_The_Endless_Frontier', 'Vannevar Bush, <i>Science, the Endless Frontier</i>') + ' (1945). The report behind postwar American science funding.',
    'The ' + wiki('DARPA', 'ARPA') + ' model: give program managers real budgets and real freedom for a few years, then rotate them out.',
    'Newer structures: ' + a('https://www.convergentresearch.org', 'focused research organizations') + ', ' + a('https://arcinstitute.org', 'Arc Institute') + ' (funds scientists for long stretches), and ' + a('https://frontierclimate.com', 'Frontier') + ' (commits to buying a product before it exists).',
    'Paul Graham, ' + a('http://www.paulgraham.com/swan.html', 'Black Swan Farming') + ' and ' + a('http://www.paulgraham.com/growth.html', 'Startup = Growth') + '.',
    'Patrick Collison and Tyler Cowen, ' + a('https://www.theatlantic.com/science/archive/2019/07/we-need-new-science-progress/594946/', 'We Need a New Science of Progress') + ' (2019).',
    wiki('Carlota_Perez', 'Carlota Perez') + ', <i>Technological Revolutions and Financial Capital</i>, on how financial bubbles fund new infrastructure.',
    'Sebastian Mallaby, <i>The Power Law</i>. William Janeway, <i>Doing Capitalism in the Innovation Economy</i>.',
    a('https://www.berkshirehathaway.com/letters/letters.html', 'Buffett&rsquo;s letters') + ' and Thorndike&rsquo;s <i>The Outsiders</i>.',
    'Bessemer&rsquo;s ' + a('https://www.bvp.com/anti-portfolio', 'anti-portfolio') + ', a list of famous companies they passed on.',
)))

# 05 bioluminescence --------------------------------------------------------
INTERESTS.append(('bioluminescence', 'Bioluminescence', [
    'Life spent billions of years in water before it reached land. That may be why most deep-sea animals make their own light and almost nothing on land does.',
    'I&rsquo;d like to engineer it on land and make our pale blue dot a little more like Pandora. ' + LAURELIN + ' is my attempt to design that light de novo.',
], notes(
    'Bioluminescence has evolved independently at least 94 times.',
    'In a ' + a('https://doi.org/10.1038/srep45750', '2017 survey') + ' of the water column off California, about three quarters of the animals observed could make light.',
    'Below about 200 metres sunlight fades; below 1,000 it&rsquo;s gone. Down there animals use light to hunt, hide, warn and find mates. Some fish light their bellies to hide their silhouette from predators below.',
) + img('dino', 'Dinoflagellates lighting up a shoreline at night.') + notes(
    'On land the list is short: fireflies, click beetles, a few millipedes and worms, and over a hundred species of glowing fungi.',
) + img('panellus', '<i>Panellus stipticus</i>, one of the glowing fungi.') + notes(
    'Almost all of it is the same reaction: an enzyme, a luciferase, oxidises a small molecule, a luciferin, and the excited product releases a photon.',
    'Two designs matter for engineering. Supply the fuel from outside, as with firefly luciferase or NanoLuc. Or let the organism make its own, as glowing mushrooms do.',
    'The mushroom pathway was ' + a('https://doi.org/10.1073/pnas.1803615115', 'mapped in 2018') + ': four enzymes turn caffeic acid into a luciferin, burn it, and recycle the remains. Plants already make caffeic acid, so the pathway moves into them. Glowing tobacco followed in 2020, ' + a('https://doi.org/10.1038/s41592-023-02152-y', 'brighter versions') + ' in 2024, and glowing petunias went on sale in the US the same year.',
    a('https://doi.org/10.1038/s41586-023-05696-3', 'Yeh et al., 2023') + ': luciferases designed from scratch with deep learning. Enzymes nature never made.',
    'A green photon at 520 nm carries about 2.4 eV, and every one costs a luciferin. A 100,000-litre lagoon glowing at 10<sup>13</sup> photons per second per litre puts out about 0.4 watts, less than a small LED.',
    'The hard part is brightness: lots of light, for a long time, without hurting the host.',
    'Light can carry information. Split luciferases glow only when two molecules meet. In 2026, ' + a('https://doi.org/10.1038/s41467-026-73810-w', 'sentinel plants') + ' that shift the colour of their glow when infected by a virus.',
    a('https://doi.org/10.1126/sciadv.adi8643', 'Living composites') + ': dinoflagellates in gels that glow when you press them.',
) + '''<figure class="fig" data-widget="glow"><canvas aria-label="Interactive field of glowing plankton"></canvas><span class="readout">move through the water</span></figure>''' + notes(
    'On Pandora, the forest floor lights up where you step. Glowing fungi, sea sparkle and fireflies already exist on Earth. I want to engineer that kind of light on land, bright enough to change how a place looks at night.',
    'The name: in Tolkien&rsquo;s <i>Silmarillion</i>, before the Sun and Moon, the world was lit by ' + wiki('Two_Trees_of_Valinor', 'two trees') + '. Telperion shone silver. Laurelin shone gold.',
    'Sep 5, 2025. ' + a('https://futurism.com/science-energy/bioengineering-plants-glow-light-cities', 'Bioengineering plants to glow and light cities') + ' (Futurism) and ' + a('https://www.piratewires.com/p/glow-in-the-dark-animals-plants-fungi', 'glow-in-the-dark animals, plants and fungi') + ' (Pirate Wires).',
)))

# 06 space economy ----------------------------------------------------------
INTERESTS.append(('space-sustainability', 'Space sustainability', [
    'Launch costs have collapsed and orbit is filling up fast. A real economy is forming above us, and so is a debris problem.',
    'One of my first research projects, in my last year of school, used machine learning to map and track debris in low Earth orbit. It won the NASA Space Apps Challenge, and I&rsquo;m still proud of it.',
], notes(
    'The Space Shuttle cost around $54,000 per kilogram to orbit. A reusable Falcon 9 costs a few thousand.',
    'Most satellites ever launched went up in the last few years.',
    'At orbital speed, about 7.5 km/s, a one-centimetre fragment hits like a hand grenade. Tens of thousands of objects are tracked. ESA estimates over a million more pieces larger than a centimetre, too small to track.',
) + img('leo', 'NASA&rsquo;s visualisation of tracked objects in low Earth orbit. Most are debris. Dots enlarged for visibility.') + notes(
    wiki('Kessler_syndrome', 'Kessler syndrome') + ' (1978): past a certain density, collisions make fragments that make more collisions.',
    '2007: a Chinese anti-satellite test destroys Fengyun-1C and creates more than 3,000 trackable fragments. 2009: Iridium 33 and the dead Kosmos 2251 collide. 2021: a Russian test destroys Kosmos 1408, and the ISS crew shelters in their spacecraft.',
    'My project: public catalogues describe every tracked object with a two-line element set. I used machine learning to predict where objects would be and flag close approaches, working from noisy and irregular observations.',
    'In 2021 Steve Wozniak co-founded Privateer with Alex Fielding to map everything in orbit, with the astrodynamicist ' + wiki('Moriba_Jah', 'Moriba Jah') + '. Jah argues orbit should be protected as an environment, like the ocean.',
    a('https://leolabs.space', 'LeoLabs') + ' tracks small objects with ground radar. ' + a('https://www.space-track.org', 'Space-Track') + ' publishes the catalogue. ' + a('https://www.esa.int/Space_Safety/Space_Debris', 'ESA') + ' publishes a yearly report on the orbital environment.',
    'Removal hardware: ' + wiki('RemoveDEBRIS', 'RemoveDEBRIS') + ' caught a target with a net and harpooned another (2018&ndash;19). ' + a('https://astroscale.com', 'Astroscale') + '&rsquo;s ELSA-d demonstrated magnetic capture (2021), and ADRAS-J flew within about 15 metres of a spent H-IIA rocket stage (2024), with a capture mission to follow. ESA&rsquo;s ' + wiki('ClearSpace-1', 'ClearSpace-1') + ' plans to grab a dead satellite with robotic arms. Starfish Space is building servicers that dock with satellites and move them.',
    'Rules: in 2022 the FCC cut the deadline for deorbiting dead satellites from 25 years to five. ESA&rsquo;s Zero Debris Charter targets 2030.',
    'Removing one large object costs tens of millions of dollars, and no single operator is responsible for the problem. I expect that to change once operators have to pay for the collision risk they add.',
    a('https://www.spaceappschallenge.org', 'NASA Space Apps Challenge') + '.',
)))

# 07 strategy games ---------------------------------------------------------
INTERESTS.append(('strategy-games', 'Strategy games', [
    'I&rsquo;ve spent thousands of hours on <i>The Battle of Polytopia</i>, been ranked in the global top 10 several times, and still play in its Diamond league.',
    'Wanting more depth, I built my own version of Azad, the game in Iain M. Banks&rsquo;s <i>The Player of Games</i>. It&rsquo;s roughly what I wish Polytopia would become.',
], notes(
    wiki('The_Battle_of_Polytopia', 'Polytopia') + ' looks simple: tribes, cities and a tech tree on a small square map. It&rsquo;s mostly a game about tempo: a city founded one turn earlier can decide a game twenty turns later.',
    'At the top level, games usually turn on a few moments where one player spots something first, like a weak flank or a tech timing.',
    'In ' + wiki('The_Player_of_Games', '<i>The Player of Games</i>') + ' (1988), the Empire of Azad uses its game to decide who holds power, up to the emperor.',
    'Banks never gives Azad&rsquo;s rules, so my version is my own guess at the depth he describes.',
    'How big games are, in legal positions: tic-tac-toe about 10<sup>3</sup>, checkers 10<sup>20</sup>, chess 10<sup>44</sup>, Go 10<sup>170</sup>.',
) + img('deepblue', 'One of the two racks of IBM&rsquo;s Deep Blue, now at the Computer History Museum.') + notes(
    '1997: Deep Blue beats Kasparov. 2016: ' + wiki('AlphaGo_versus_Lee_Sedol', 'AlphaGo beats Lee Sedol') + '; move 37 in game two looked like a mistake to every expert watching. 2019: AlphaStar reaches grandmaster in StarCraft II, and Pluribus beats professionals at six-player poker. 2022: Meta&rsquo;s ' + a('https://ai.meta.com/research/cicero/', 'CICERO') + ' plays Diplomacy, a game of negotiation, at human level.',
)))

# 08 planetary engineering --------------------------------------------------
INTERESTS.append(('planetary-engineering', 'Planetary engineering', [
    'Rain where it&rsquo;s needed, carbon pulled out of the air and turned to stone, and other ways of steering the climate deliberately. ' + a('https://www.rainmaker.com', 'Rainmaker') + ' is a good example.',
    'I like thinking about which futures Earth could still have.',
], notes(
    '1946: Vincent Schaefer at General Electric drops dry ice into a cloud from a plane and makes it snow. ' + wiki('Cloud_seeding', 'Cloud seeding') + ' stayed controversial for decades because the effect was hard to measure.',
    a('https://www.rainmaker.com', 'Rainmaker') + ', founded by Augustus Doricko, seeds clouds with drones and measures the result with radar. If it works reliably, a dry region gets more of the water already passing overhead.',
    'Carbon removal, by permanence. Direct air capture: ' + a('https://climeworks.com', 'Climeworks') + ' in Iceland, paired with ' + a('https://www.carbfix.com', 'Carbfix') + ', which injects CO<sub>2</sub> into basalt where it turns to stone within about two years. ' + a('https://www.heirloomcarbon.com', 'Heirloom') + ' uses limestone.',
    wiki('Enhanced_weathering', 'Enhanced weathering') + ': spread crushed basalt or olivine and let the rock cycle run faster. ' + a('https://charmindustrial.com', 'Charm') + ' turns crop waste into bio-oil and pumps it underground.',
    a('https://frontierclimate.com', 'Frontier') + ' (Stripe, Google, Shopify, Meta, McKinsey, 2022) committed nearly a billion dollars to buy permanent carbon removal in advance.',
) + img('pinatubo', 'Mount Pinatubo, June 12, 1991. The eruption cooled the planet by about half a degree for more than a year.') + notes(
    wiki('Solar_geoengineering', 'Solar geoengineering') + ' would do on purpose what Pinatubo did by accident. It would be cheap and fast, and one country could do it alone, which is why it&rsquo;s contentious.',
    a('https://terraformindustries.com', 'Terraform Industries') + ' (Casey Handmer): natural gas made from sunlight and air.',
    'Three futures: slow decarbonisation and expensive adaptation; cheap clean energy plus removal bringing CO<sub>2</sub> back down; or a climate managed like a city&rsquo;s water supply, monitored, adjusted and boring.',
    'Kim Stanley Robinson has written about both Earth and Mars: ' + wiki('The_Ministry_for_the_Future', '<i>The Ministry for the Future</i>') + ' and ' + wiki('Mars_trilogy', '<i>Red Mars</i>') + '.',
    a('https://ourworldindata.org/co2-and-greenhouse-gas-emissions', 'Our World in Data') + ' for the numbers.',
)))

# 09 aesthetics -------------------------------------------------------------
INTERESTS.append(('aesthetics', 'Aesthetics', [
    'People take care of the places and things they find beautiful.',
    'I&rsquo;m most drawn to solarpunk: architecture where technology and living things grow together. ' + LAURELIN + ' is partly my way of contributing to it.',
], notes(
    'Much of what we&rsquo;ve built in the last century is uglier than what it replaced, even though we&rsquo;re far richer.',
    wiki('Solarpunk', 'Solarpunk') + ' started around 2008 as a fiction genre and turned into an aesthetic: advanced technology combined with plants, gardens and green space. Art Nouveau and Studio Ghibli are in its family tree.',
) + img('supertree', 'Supertree Grove at Gardens by the Bay, Singapore. Steel structures up to 50 metres tall, covered in living plants.') + notes(
    wiki('Bosco_Verticale', 'Bosco Verticale') + ', Stefano Boeri, Milan, 2014: two residential towers carrying hundreds of trees on their balconies.',
    'Singapore has gone furthest. WOHA&rsquo;s ' + wiki('Kampung_Admiralty', 'Kampung Admiralty') + ' stacks a park, a clinic and housing for older people into one building. Safdie&rsquo;s ' + wiki('Jewel_Changi_Airport', 'Jewel') + ' wraps a forest around an indoor waterfall.',
    wiki('Friedensreich_Hundertwasser', 'Hundertwasser') + ' was putting trees on roofs, and refusing straight lines, in Vienna decades earlier.',
    'At night these buildings are floodlit like any other. I&rsquo;d like to see streets and walls lit by the plants growing on them.',
    'Christopher Alexander, ' + wiki('A_Pattern_Language', '<i>A Pattern Language</i>') + '. Becky Chambers, ' + wiki('A_Psalm_for_the_Wild-Built', '<i>A Psalm for the Wild-Built</i>') + '. <i>Sunvault</i> (2017). ' + a('https://solar.lowtechmagazine.com', 'Low-tech Magazine') + ', a solar-powered website.',
)))
