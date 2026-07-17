"""
Builds movies.csv: a curated set of well-known films spanning many genres/eras.
Descriptions are short, original summaries (not copied from any source) written
purely to give the content-based model text to work with.
"""
import csv

MOVIES = [
    # (title, year, genres(list), short_description)
    ("The Shawshank Redemption", 1994, ["Drama"], "A wrongly convicted banker forms an unlikely friendship and quietly plans an escape from a brutal prison."),
    ("The Godfather", 1972, ["Drama", "Crime"], "A mafia patriarch hands control of his empire to his reluctant youngest son."),
    ("The Dark Knight", 2008, ["Action", "Crime", "Drama"], "A vigilante battles a chaos-driven criminal mastermind for the soul of a corrupt city."),
    ("Pulp Fiction", 1994, ["Crime", "Drama"], "Interlocking stories of hitmen, boxers, and gangsters unfold with dark humor and nonlinear timing."),
    ("Forrest Gump", 1994, ["Drama", "Romance"], "A kind-hearted, slow-witted man stumbles through decades of American history and love."),
    ("Inception", 2010, ["Sci-Fi", "Action", "Thriller"], "A thief who steals secrets from dreams is offered a chance to plant an idea instead."),
    ("The Matrix", 1999, ["Sci-Fi", "Action"], "A hacker discovers reality is a simulation and joins a rebellion against machine overlords."),
    ("Fight Club", 1999, ["Drama", "Thriller"], "An insomniac office worker and a soap salesman build an underground fighting movement."),
    ("Interstellar", 2014, ["Sci-Fi", "Drama", "Adventure"], "A pilot leads a mission through a wormhole to find humanity a new home among the stars."),
    ("The Lord of the Rings: The Fellowship of the Ring", 2001, ["Fantasy", "Adventure"], "A hobbit and his companions set out to destroy a ring that could doom the world."),
    ("Star Wars", 1977, ["Sci-Fi", "Adventure"], "A farm boy joins rebels to rescue a princess and destroy a planet-killing battle station."),
    ("Goodfellas", 1990, ["Crime", "Drama"], "A young man rises through the ranks of the mob and watches his world unravel."),
    ("The Silence of the Lambs", 1991, ["Thriller", "Horror", "Crime"], "A trainee FBI agent consults an imprisoned cannibal to catch a serial killer."),
    ("Se7en", 1995, ["Thriller", "Crime"], "Two detectives hunt a killer who stages murders around the seven deadly sins."),
    ("Gladiator", 2000, ["Action", "Drama"], "A betrayed Roman general becomes a gladiator to avenge his family and defy an emperor."),
    ("The Departed", 2006, ["Crime", "Thriller"], "An undercover cop and a mob mole race to expose each other inside the Boston underworld."),
    ("Whiplash", 2014, ["Drama", "Music"], "A driven young drummer clashes with a ruthless instructor obsessed with greatness."),
    ("Parasite", 2019, ["Drama", "Thriller", "Comedy"], "A poor family cons its way into a wealthy household with unexpected consequences."),
    ("The Green Mile", 1999, ["Drama", "Fantasy"], "A death row guard discovers a condemned man possesses a miraculous gift."),
    ("Saving Private Ryan", 1998, ["War", "Drama"], "A squad of soldiers is sent behind enemy lines to bring one man home from war."),
    ("Schindler's List", 1993, ["Drama", "War", "History"], "A German businessman gradually risks everything to save Jewish workers during the Holocaust."),
    ("The Prestige", 2006, ["Drama", "Mystery", "Sci-Fi"], "Two rival stage magicians escalate their feud into obsession and sabotage."),
    ("The Usual Suspects", 1995, ["Crime", "Mystery", "Thriller"], "A small-time con man recounts a heist gone wrong tied to a mythic crime lord."),
    ("Memento", 2000, ["Mystery", "Thriller"], "A man with short-term memory loss hunts his wife's killer using notes and tattoos."),
    ("The Prestige II placeholder", 2050, ["Placeholder"], "placeholder"),
]
# remove placeholder row (kept list generation simple above)
MOVIES = [m for m in MOVIES if m[1] != 2050]

MORE = [
    ("Eternal Sunshine of the Spotless Mind", 2004, ["Romance", "Sci-Fi", "Drama"], "A heartbroken man undergoes a procedure to erase memories of a failed relationship."),
    ("La La Land", 2016, ["Romance", "Music", "Drama"], "An aspiring actress and a jazz pianist chase their dreams while falling in love in Los Angeles."),
    ("Amelie", 2001, ["Romance", "Comedy"], "A whimsical Parisian waitress secretly orchestrates happiness for those around her."),
    ("Titanic", 1997, ["Romance", "Drama"], "A penniless artist and a wealthy young woman fall in love aboard a doomed ocean liner."),
    ("Pride and Prejudice", 2005, ["Romance", "Drama"], "A spirited young woman navigates class, family, and misjudged first impressions in love."),
    ("Notting Hill", 1999, ["Romance", "Comedy"], "A humble bookshop owner falls for a famous actress who wanders into his shop."),
    ("500 Days of Summer", 2009, ["Romance", "Comedy", "Drama"], "A greeting-card writer looks back on a relationship that didn't end the way he hoped."),
    ("The Notebook", 2004, ["Romance", "Drama"], "A summer romance between two young lovers is tested by class and time."),
    ("Superbad", 2007, ["Comedy"], "Two inseparable best friends scramble through one chaotic night before graduation."),
    ("Bridesmaids", 2011, ["Comedy"], "A maid of honor's life unravels while she tries to plan her best friend's wedding."),
    ("The Grand Budapest Hotel", 2014, ["Comedy", "Adventure"], "A legendary concierge and his protege get tangled in a stolen painting and a family feud."),
    ("Groundhog Day", 1993, ["Comedy", "Fantasy", "Romance"], "A cynical weatherman relives the same day until he learns to actually live it."),
    ("Ferris Bueller's Day Off", 1986, ["Comedy"], "A charming high schooler fakes sick and turns a day of freedom into an urban adventure."),
    ("The Hangover", 2009, ["Comedy"], "Three friends piece together a wild bachelor-party night after losing the groom."),
    ("Knives Out", 2019, ["Mystery", "Comedy", "Crime"], "A famous detective unravels a web of lies after a wealthy novelist's suspicious death."),
    ("Get Out", 2017, ["Horror", "Thriller", "Mystery"], "A young man uncovers a sinister secret during a visit to his girlfriend's family estate."),
    ("Hereditary", 2018, ["Horror", "Drama"], "A family unravels as dark, inherited secrets resurface after a devastating loss."),
    ("A Quiet Place", 2018, ["Horror", "Sci-Fi", "Thriller"], "A family survives in silence to avoid blind creatures that hunt by sound."),
    ("The Conjuring", 2013, ["Horror", "Thriller"], "Paranormal investigators help a haunted family confront a malevolent presence."),
    ("It", 2017, ["Horror", "Fantasy"], "A group of kids confronts a shape-shifting entity that preys on their small town."),
    ("28 Days Later", 2002, ["Horror", "Sci-Fi"], "A man wakes from a coma into a Britain ravaged by a rage-driven infection."),
    ("Alien", 1979, ["Horror", "Sci-Fi"], "A commercial spaceship crew is hunted by a deadly extraterrestrial stowaway."),
    ("Jurassic Park", 1993, ["Adventure", "Sci-Fi"], "A theme park of cloned dinosaurs spirals into chaos when the systems fail."),
    ("Back to the Future", 1985, ["Sci-Fi", "Adventure", "Comedy"], "A teenager is accidentally sent to the past and must repair the timeline of his own family."),
    ("E.T. the Extra-Terrestrial", 1982, ["Sci-Fi", "Family", "Adventure"], "A boy befriends a stranded alien and helps him find a way home."),
    ("Guardians of the Galaxy", 2014, ["Sci-Fi", "Action", "Comedy"], "A ragtag crew of misfits bands together to stop a fanatic from destroying a planet."),
    ("Mad Max: Fury Road", 2015, ["Action", "Sci-Fi", "Adventure"], "A rebel driver and a warrior escape a tyrant across a relentless desert wasteland."),
    ("John Wick", 2014, ["Action", "Thriller", "Crime"], "A retired hitman seeks vengeance against the men who wronged him."),
    ("Die Hard", 1988, ["Action", "Thriller"], "An off-duty cop battles terrorists who seize a skyscraper during a Christmas party."),
    ("The Bourne Identity", 2002, ["Action", "Thriller", "Mystery"], "An amnesiac trained assassin races to uncover his own identity before his handlers find him."),
    ("Mission: Impossible - Fallout", 2018, ["Action", "Thriller"], "A covert agent races to stop a plot involving stolen plutonium and old betrayals."),
    ("Casino Royale", 2006, ["Action", "Thriller"], "A newly minted secret agent takes on a financier of global terrorism in a high-stakes card game."),
    ("Skyfall", 2012, ["Action", "Thriller"], "An aging agent confronts a personal vendetta threatening the intelligence service itself."),
    ("Black Panther", 2018, ["Action", "Sci-Fi", "Adventure"], "A new king must defend his technologically advanced nation from a vengeful challenger."),
    ("The Avengers", 2012, ["Action", "Sci-Fi", "Adventure"], "Earth's mightiest heroes assemble to stop an alien invasion led by a vengeful god."),
    ("Spider-Man: Into the Spider-Verse", 2018, ["Animation", "Action", "Adventure"], "A teenager from Brooklyn discovers he shares his destiny with spider-heroes from other dimensions."),
    ("Toy Story", 1995, ["Animation", "Family", "Comedy"], "A cowboy doll's world is upended when a flashy spaceman toy becomes his owner's favorite."),
    ("Finding Nemo", 2003, ["Animation", "Family", "Adventure"], "An anxious clownfish crosses the ocean to rescue his son from an aquarium tank."),
    ("Up", 2009, ["Animation", "Adventure", "Family"], "An elderly widower ties balloons to his house and flies off on the adventure he always promised."),
    ("Coco", 2017, ["Animation", "Family", "Fantasy"], "A boy who dreams of music crosses into the Land of the Dead to uncover his family's true history."),
    ("Spirited Away", 2001, ["Animation", "Fantasy", "Adventure"], "A young girl works in a spirit-world bathhouse to save her parents from a curse."),
    ("Inside Out", 2015, ["Animation", "Family", "Comedy"], "Personified emotions steer a young girl through the upheaval of moving to a new city."),
    ("The Lion King", 1994, ["Animation", "Family", "Drama"], "A lion cub flees his kingdom after his father's death and must reclaim his throne."),
    ("Shrek", 2001, ["Animation", "Comedy", "Fantasy"], "A grumpy ogre reluctantly rescues a princess to reclaim his swamp from a scheming lord."),
    ("How to Train Your Dragon", 2010, ["Animation", "Family", "Adventure"], "A young Viking befriends the dragon he was raised to slay and changes his village forever."),
    ("Whiplash II placeholder", 2050, ["Placeholder"], "placeholder"),
]
MORE = [m for m in MORE if m[1] != 2050]

EVEN_MORE = [
    ("Django Unchained", 2012, ["Western", "Drama"], "A freed slave partners with a bounty hunter to rescue his wife from a ruthless plantation owner."),
    ("No Country for Old Men", 2007, ["Thriller", "Crime", "Western"], "A hunter who stumbles on drug money is stalked by an unstoppable killer across the desert."),
    ("The Good, the Bad and the Ugly", 1966, ["Western"], "Three gunslingers race to find a fortune in gold buried during the Civil War."),
    ("Unforgiven", 1992, ["Western", "Drama"], "A retired gunfighter takes one last job that forces him to confront his violent past."),
    ("12 Years a Slave", 2013, ["Drama", "History"], "A free Black man is kidnapped and sold into slavery in the antebellum South."),
    ("The Social Network", 2010, ["Drama", "History"], "The founding of a world-changing company fractures the friendship at its center."),
    ("The Wolf of Wall Street", 2013, ["Drama", "Comedy", "Crime"], "A stockbroker's rise and fall is fueled by fraud, excess, and unchecked ambition."),
    ("A Beautiful Mind", 2001, ["Drama", "Biography"], "A brilliant mathematician struggles with schizophrenia while making groundbreaking discoveries."),
    ("The Imitation Game", 2014, ["Drama", "History", "Thriller"], "A socially awkward mathematician races to crack a Nazi code that could end the war."),
    ("Dune", 2021, ["Sci-Fi", "Adventure"], "A young heir is thrust into a war over a desert planet that holds the universe's most valuable resource."),
    ("Blade Runner 2049", 2017, ["Sci-Fi", "Thriller"], "A replicant detective uncovers a secret that could unravel the fragile order between humans and machines."),
    ("Arrival", 2016, ["Sci-Fi", "Drama", "Mystery"], "A linguist is recruited to communicate with mysterious visitors before global panic turns to war."),
    ("Ex Machina", 2014, ["Sci-Fi", "Drama", "Thriller"], "A programmer is invited to test whether an android's mind is truly conscious."),
    ("Her", 2013, ["Sci-Fi", "Romance", "Drama"], "A lonely writer falls in love with an intelligent operating system designed to meet his every need."),
    ("Children of Men", 2006, ["Sci-Fi", "Drama", "Thriller"], "In a world where no child has been born for years, one man protects humanity's last hope."),
    ("The Truman Show", 1998, ["Drama", "Comedy", "Sci-Fi"], "A man slowly realizes his entire life has been broadcast as a reality show."),
    ("Requiem for a Dream", 2000, ["Drama"], "Four intertwined lives spiral into addiction with devastating consequences."),
    ("American Beauty", 1999, ["Drama"], "A suburban father's midlife crisis unravels the quiet dysfunction of his family."),
    ("There Will Be Blood", 2007, ["Drama"], "An oil prospector's ruthless ambition consumes everyone around him."),
    ("Moonlight", 2016, ["Drama"], "A young man's identity and sexuality unfold across three chapters of his life in Miami."),
    ("Manchester by the Sea", 2016, ["Drama"], "A withdrawn handyman is forced to confront old grief when he becomes his nephew's guardian."),
    ("The Pianist", 2002, ["Drama", "War", "Biography"], "A Jewish pianist struggles to survive the destruction of Warsaw during World War II."),
    ("Slumdog Millionaire", 2008, ["Drama", "Romance"], "A young man from the Mumbai slums recounts the life story behind his game-show success."),
    ("City of God", 2002, ["Drama", "Crime"], "Two boys take different paths through decades of gang violence in a Rio favela."),
    ("Oldboy", 2003, ["Thriller", "Mystery", "Drama"], "A man seeks revenge after being inexplicably imprisoned alone for fifteen years."),
    ("Prisoners", 2013, ["Thriller", "Drama", "Mystery"], "A desperate father takes matters into his own hands after his daughter's abduction."),
    ("Gone Girl", 2014, ["Thriller", "Mystery", "Drama"], "A man becomes the prime suspect when his wife vanishes on their anniversary."),
    ("Zodiac", 2007, ["Thriller", "Crime", "Mystery"], "A cartoonist becomes obsessed with identifying a serial killer taunting the police with ciphers."),
    ("Shutter Island", 2010, ["Thriller", "Mystery"], "A U.S. Marshal investigates a disappearance at an isolated hospital for the criminally insane."),
    ("The Sixth Sense", 1999, ["Thriller", "Drama", "Mystery"], "A troubled child psychologist tries to help a boy who claims he can see the dead."),
    ("Coraline", 2009, ["Animation", "Fantasy", "Horror"], "A girl discovers an idealized parallel world hiding a sinister truth behind a small door."),
    ("WALL-E", 2008, ["Animation", "Sci-Fi", "Family"], "A lonely trash-collecting robot on a ruined Earth finds purpose chasing a sleek probe from space."),
    ("Ratatouille", 2007, ["Animation", "Comedy", "Family"], "A rat with a gift for cooking secretly guides a clumsy chef through a Parisian kitchen."),
    ("Zootopia", 2016, ["Animation", "Comedy", "Mystery"], "A rookie rabbit officer and a con-artist fox uncover a conspiracy in a city of anthropomorphic animals."),
    ("Kung Fu Panda", 2008, ["Animation", "Action", "Comedy"], "An unlikely panda is chosen as a legendary warrior meant to protect his valley."),
    ("Moana", 2016, ["Animation", "Adventure", "Family"], "A chief's daughter sails beyond her reef to save her island alongside a fallen demigod."),
    ("Frozen", 2013, ["Animation", "Family", "Fantasy"], "A princess sets out to find her sister, whose icy powers have plunged their kingdom into eternal winter."),
    ("Your Name", 2016, ["Animation", "Romance", "Fantasy"], "Two teenagers mysteriously swap bodies and race against time to meet before a looming disaster."),
    ("Whiplash III placeholder", 2050, ["Placeholder"], "placeholder"),
]
EVEN_MORE = [m for m in EVEN_MORE if m[1] != 2050]

ALL_MOVIES = MOVIES + MORE + EVEN_MORE

with open("/home/claude/movie-recommender/backend/data/movies.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["movie_id", "title", "year", "genres", "overview"])
    for i, (title, year, genres, overview) in enumerate(ALL_MOVIES, start=1):
        writer.writerow([i, title, year, "|".join(genres), overview])

print(f"Wrote {len(ALL_MOVIES)} movies")
