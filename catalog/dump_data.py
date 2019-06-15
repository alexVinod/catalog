from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from novels_db import *
import json


engine = create_engine('sqlite:///books.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Deleting OurUsers if existing.
session.query(OurUsers).delete()


session.query(BookStoreCategory).delete()

# Deleting Books if exisitng.
session.query(Books).delete()


# ---OurOwners DataDump---
ourUsers = [{"email": "alex.apssdc@gmail.com",
             "id": 1,
             "name": "vinod pasupuleti",
             "picture": "https://lh6.googleusercontent.com\
             /-DPxolQWkRoU/AAAAAAAAAAI/AAAAAAAA\
             AE0/7p3dhkp9fso/s96-c/photo.jpg"},
            {"email": "pasupuletivinod8@gmail.com",
             "id": 2,
             "name": "Vinod Pasupuleti",
             "picture": "https://lh3.googleusercontent.com\
             /-PqcAhX6BmIk/AAAAAAAAA\
             AI/AAAAAAAAABY/Yy4rTTdoCQY/photo.jpg"},
            {"email": "vinodcrackworld@gmail.com",
             "id": 3,
             "name": "vinod Pasupuleti",
             "picture": "https://lh3.googleusercontent.com\
             /-NV7E_Dzez2I/AAAAAAAAA\
             AI/AAAAAAAAAFc/RiBSmLwSpgg/photo.jpg"}]

owners = []
for i in range(0, len(ourUsers)):
    # print(book["title"],book["author"],book["bookType"],book["description"],book["publishedDate"],book["publisher"],book["imageLinks"],book["infoLink"],book["category_id"])
    owners.append(ourUsers[i]['name'].replace(' ', '') + str(i))
    owners[i] = OurUsers(name=ourUsers[i]["name"], email=ourUsers[i]
                         ["email"], picture=ourUsers[i]["picture"])
    session.add(owners[i])
    session.commit()
    print(owners[i])

# ---BookShelf DataDump---

categorys = ["Art", "Action", "Business", "Comics", "Cook",
             "Design", "Education", "Robotics", "Time", "Virtual Reality"]
bookShelf = [
    {
        "category": "Art",
        "ourUser_id": 2
    },
    {
        "category": "Action",
        "ourUser_id": 1
    },

    {
        "category": "Comics",
        "ourUser_id": 1
    },
    {
        "category": "Cook",
        "ourUser_id": 1
    },
    {
        "category": "Design",
        "ourUser_id": 2
    },
    {
        "category": "Education",
        "ourUser_id": 1
    },

    {
        "category": "Time",
        "ourUser_id": 2
    },
    {
        "category": "Virtual Reality",
        "ourUser_id": 1
    },
    {
        "category": "God",
        "ourUser_id": 1
    }
]


shelfs = []
for i in range(0, len(bookShelf)):
    # print(book["title"],book["author"],book["bookType"],book["description"],book["publishedDate"],book["publisher"],book["imageLinks"],book["infoLink"],book["category_id"])
    shelfs.append(bookShelf[i]['category'].replace(' ', ''))
    shelfs[i] = BookStoreCategory(
        category=bookShelf[i]["category"],
        ourUser_id=bookShelf[i]["ourUser_id"])
    session.add(shelfs[i])
    session.commit()
    # print(shelfs[i].ourUser_id,shelfs[i].category)


# ---Books DataDump---
books = [{"author": "Nils HartmannOliver Zeigermann",
          "bookType": "Education",
          "category_id": 6,
          "description": "React ist ein JavaScript-Framework\
           zur Entwicklung von \
           Benutzeroberflächen sowohl im \
           Browser als auch auf Mobilgeräten. \
           Entwickelt und eingesetzt von \
           Facebook ist es mittlerweile als \
           Open-Source-Projekt verfügbar und hat sich \
           bereits im Einsatz bei diversen namhaften Websites, \
           wie z. B. Airbnb und Netflix, bewährt. \
           Dieses Buch stellt Ihnen die Konzepte von React, React \
           Router und Redux anhand eines durchgehenden Beispiels vor. \
           Sie lernen, wie Sie mit React wiederverwendbare \
           UI-Komponenten entwickeln und wie Sie auf Basis der \
           einzelnen Komponenten ganze Anwendungen \
           zusammenbauen. Unter anderem werden \
           folgende Themen behandelt: - \
           Entwickeln und Testen eigener \
           React-Komponenten auf Basis des \
           JavaScript-Standards ECMAScript 2015 (ES6) - \
           Routing mit dem React Router - \
           Das Architektur-Modell \
           Flux und wie damit komplette Anwendungen \
           umgesetzt werden \
           (am Beispiel des Redux-Frameworks) - \
           Serverseitiges Rendern von \
           React-Komponenten und -Anwendungen - \
           Anbindung eines REST-Backends \
           Die im Buch eingesetzten Sprachfeatures \
           aus ES6 werden in einem eigenen \
           Kapitel vorgestellt, sodass \
           zum Verständnis des Buches \
           Kenntnisse von ES5 ausreichen. \
           Nach der Lektüre des Buches \
           werden Sie in der Lage sein, \
           eigene Projekte mit React umzusetzen.",
          "imageLinks": "react.jpg",
          "infoLink": "https://books.google.co.in/books?id=IOejDAAAQBAJ&dq=\
          redux+react&hl=&source=gb\
          s_api&redir_esc=y",
          "ourUser_id": 2,
          "publishedDate": "April 20, 2019",
          "publisher": "VinodBooks",
          "title": "React 1.6"},
         {"author": "Nils HartmannOliver Zeigermann",
          "bookType": "Education",
          "category_id": 6,
          "description": "React ist ein \
          JavaScript-Framework zur Entwicklung von \
          Benutzeroberflächen sowohl im \
          Browser als auch auf Mobilgeräten. \
          Entwickelt und eingesetzt von Facebook \
          ist es mittlerweile als Open-Source-Projekt \
          verfügbar und hat sich bereits im Einsatz \
          bei diversen namhaften Websites, \
          wie z. B. Airbnb und Netflix, \
          bewährt. Dieses Buch stellt Ihnen die \
          Konzepte von React, React Router und Redux \
          anhand eines durchgehenden Beispiels vor. \
          Sie lernen, wie Sie mit React \
          wiederverwendbare UI-Komponenten \
          entwickeln und wie Sie auf Basis \
          der einzelnen Komponenten ganze \
          Anwendungen zusammenbauen. \
          Unter anderem werden folgende \
          Themen behandelt: - Entwickeln und \
          Testen eigener React-Komponenten \
          auf Basis des JavaScript-Standards \
          ECMAScript 2015 (ES6) - Routing mit \
          dem React Router - Das Architektur-Modell \
          Flux und wie damit komplette Anwendungen \
          umgesetzt werden \
          (am Beispiel des Redux-Frameworks) - \
          Serverseitiges Rendern von React-Komponenten und \
          -Anwendungen - Anbindung eines REST-Backends \
          Die im Buch eingesetzten Sprachfeatures aus ES6 werden in einem \
          eigenen Kapitel vorgestellt, sodass zum Verständnis \
          des Buches Kenntnisse von ES5 ausreichen. \
          Nach der Lektüre des Buches werden \
          Sie in der Lage sein, eigene \
          Projekte mit React umzusetzen.",
          "imageLinks": "react2.jpg",
          "infoLink": "https://books.google.co.in\
          /books?id=IOejDAAAQBAJ&dq=redux+r\
          eact&hl=&source=gbs_api&redir_esc=y",
          "ourUser_id": 2,
          "publishedDate": "April 20, 2019",
          "publisher": "VinodBooks",
          "title": "React 2.0"},
         {"author": "Google & Microsoft",
          "bookType": "Education",
          "category_id": 6,
          "description": "Angular is a platform \
          that makes it easy to build \
          applications with the web. Angular \
          combines declarative templates, \
          dependency injection, end to end tooling, \
          and integrated best practices \
          to solve development challenges. \
          Angular empowers developers to \
          build applications that live \
          on the web, mobile, or the desktop.",
          "imageLinks": "angular.svg",
          "infoLink": "https://angular.io/docs",
          "ourUser_id": 2,
          "publishedDate": "Jan 20, 2019",
          "publisher": "angular.io",
          "title": "Angular 7 ( Stable )"},
         {"author": "Evan You",
          "bookType": "Education",
          "category_id": 6,
          "description": "Vue (pronounced /vjuː/, like view) \
          is a progressive framework for \
          building user interfaces. \
          Unlike other monolithic frameworks, \
          Vue is designed from the ground up \
          to be incrementally adoptable. \
          The core library is focused on the \
          view layer only, and is easy to \
          pick up and integrate with other \
          libraries or existing projects. \
          On the other hand, Vue is also \
          perfectly capable of powering \
          sophisticated Single-Page \
          Applications when used in \
          combination with modern tooling \
          and supporting libraries.",
          "imageLinks": "vueJs.png",
          "infoLink": "https://vuejs.org/",
          "ourUser_id": 2,
          "publishedDate": "Jan 21, 2019",
          "publisher": "https://vuejs.org/",
          "title": "Vue JS"},
         {"author": "Zed A.Shaw ",
          "bookType": "Education",
          "category_id": 6,
          "description": "You Will Learn Python 3! \
          Zed Shaw has perfected the world’s \
          best system for learning Python 3. \
          Follow it and you will succeed—just \
          like the millions of beginners Zed has \
          taught to date! You bring the discipline, \
          commitment, and persistence; the \
          author supplies everything else.",
          "imageLinks": "python3.jpg",
          "infoLink": "https://www.amazon.in/Learn-\
          Python-3-Hard-Way/dp/9352865103/ref=sr\
          _1_1?ie=UTF8&qid=1551091042&sr=8\
          -1&keywords=python+books",
          "ourUser_id": 2,
          "publishedDate": "Jan 23, 2019",
          "publisher": " Pearson Education; \
          First Edition edition (2017)",
          "title": "Learn Python 3 The Hard Way"},
         {"author": "Alan Davis",
          "bookType": "Comics",
          "category_id": 3,
          "description": "The Avengers are a \
          fictional team of superheroes \
          appearing in American comic \
          books published by Marvel Comics. \
          The team made its debut in The \
          Avengers #1 (cover-dated Sept. 1963), \
          created by writer-editor Stan Lee \
          and artist/co-plotter Jack Kirby, \
          inspired by the success of DC \
          Comics' Justice League of America. \
          Labeled \"Earth's Mightiest Heroes\", \
          the Avengers originally consisted of \
          Ant-Man, the Hulk, Iron Man, Thor, \
          and the Wasp. Ant-Man had become \
          Giant-Man by issue #2. The original \
          Captain America was discovered trapped \
          in ice in issue #4, and joined the \
          group after they revived him. A \
          rotating roster became a hallmark \
          of the series, although one theme remained \
          consistent: the Avengers fight \"the foes no \
          single superhero can withstand.\" \
          The team, famous for its battle \
          cry of \"Avengers Assemble!\", has \
          featured humans, mutants, Inhumans, \
          androids, aliens, supernatural \
          beings, and even",
          "imageLinks": "avengers.jpg",
          "infoLink": "https://www.marvel.com/",
          "ourUser_id": 1,
          "publishedDate": "Mar 18, 2020",
          "publisher": "MarvelStudio",
          "title": "Avengers"},
         {"author": "Alan Davis",
          "bookType": "Action",
          "category_id": 2,
          "description": "The Avengers are a \
          fictional team of superheroes appearing \
          in American comic books published by \
          Marvel Comics. The team made \
          its debut in The Avengers #1 \
          (cover-dated Sept. 1963), \
          created by writer-editor \
          Stan Lee and artist/co-plotter Jack \
          Kirby, inspired by the success of DC \
          Comics' Justice League of America. \
          Labeled \"Earth's Mightiest Heroes\", the Avengers \
          originally consisted of Ant-Man, the Hulk, \
          Iron Man, Thor, and the Wasp. Ant-Man had become \
          Giant-Man by issue #2. The original Captain \
          America was discovered trapped in ice in \
          issue #4, and joined the group after they \
          revived him. A rotating roster \
          became a hallmark of the series, \
          although one theme remained consistent: \
          the Avengers fight \"the foes \
          no single superhero can withstand.\" \
          The team, famous for its battle \
          cry of \"Avengers Assemble!\", has featured \
          humans, mutants, Inhumans, androids, \
          aliens, supernatural beings, and even",
          "imageLinks": "capM.jpg",
          "infoLink": "https://www.marvel.com/",
          "ourUser_id": 1,
          "publishedDate": "Mar 18, 2020",
          "publisher": "MarvelStudio",
          "title": "Captain Marvel"},
         {"author": "Alan Davis",
          "bookType": "Action",
          "category_id": 2,
          "description": "After the events of Captain \
          America: Civil War, Prince T'Challa \
          returns home to the reclusive, \
          technologically advanced African nation \
          of Wakanda to serve as his country's new king. \
          However, T'Challa soon finds that he \
          is challenged for the throne from \
          factions within his own country. When \
          two foes conspire to destroy Wakanda, the \
          hero known as Black Panther must \
          team up with C.I.A. agent Everett K. Ross \
          and members of the Dora Milaje, Wakandan \
          special forces, to prevent Wakanda from \
          being dragged into a world war.",
          "imageLinks": "wakanda.jpg",
          "infoLink": "https://www.marvel.com/",
          "ourUser_id": 1,
          "publishedDate": "Mar 18, 2020",
          "publisher": "MarvelStudio",
          "title": "Black Panther"},
         {"author": "ABCDEF",
          "bookType": "Art",
          "category_id": 1,
          "description": "ABC",
          "imageLinks": "https://tse3.m\
          m.bing.net/th?id=OIP.8Ig\
          zot98yBAzXhdMMQMwqwHaE7&pid=Api",
          "infoLink": "ABC",
          "ourUser_id": 1,
          "publishedDate": "02/05/2019",
          "publisher": "ABC",
          "title": "ABCDEF "},
         {"author": "Uma Raghuraman",
          "bookType": "Cook",
          "category_id": 4,
          "description": "This is a delicious sweet \
          recipe which required milk and \
          sugar.Instant Palkova is quick \
          version of 'Palkova' or Palgova' which is \
          a popular South Indian sweet. This recipe \
          is believed to have originated in Tamil Nadu. \
          Due to the white revolution, the excess \
          milk was being made into Palkova. \
          It is also served to the \
          devotees visiting the Srivilliputur \
          Andal Temple in which city the origin \
          of Palkova specifically dates back to. \
          Palkova is made from just two ingredients, \
          milk and sugar. As easy as it may sound, \
          making palgova requires a lot of \
          patience.Milk is boiled and continuously \
          stirred in a heavy bottom pan/kadai till the \
          fats separate . While the traditional way of \
          making this sweet may intimidate you, today \
          I am sharing an easy and quick version \
          of making this incredibly delicious sweet. \
          Tasty, grainy milk sweet is sure to \
          transport you to food heaven. Whether it is \
          pooja, festival at home or guests coming home \
          for lunch, this handy 5-minute recipe \
          is a sure blessing.",
          "imageLinks": "https://www.archanask\
          itchen.com/images/archanaskit\
          chen/1-Author/Uma_Raghuraman/Instant_\
          Palkova_Recipe.jpg",
          "infoLink": "https://www.archanaskitc\
          hen.com/instant-palkova-rec\
          ipe-milk-based-sweet-recipe",
          "ourUser_id": 1,
          "publishedDate": "2019-02-28",
          "publisher": "Archana's Kitchen",
          "title": "Instant Palkova Recipe (Milk Based Sweet Recipe)"},
         {"author": "Uma Raghuraman",
          "bookType": "Cook",
          "category_id": 4,
          "description": "This is a delicious \
          sweet recipe which required milk and sugar. \
          Instant Palkova is a quick version of \
          'Palkova' or Palgova' which is a popular \
          South Indian sweet. This recipe is believed \
          to have originated in Tamil Nadu. Due to the white \
          revolution, excess milk was being made into \
          Palkova. It is also served to the devotees \
          visiting the Srivilliputur Andal Temple \
          in which city the origin of Palkova \
          specifically dates back to. Palkova \
          is made from just two ingredients, \
          milk, and sugar. As easy as it may \
          sound, making palgova requires a lot \
          of patience. Milk is boiled and \
          continuously stirred in a heavy \
          bottom pan/Kadai till the fats separate. \
          While the traditional way of making \
          this sweet may intimidate you, today \
          I am sharing an easy and quick \
          version of making this incredibly \
          delicious sweet. Tasty, grainy milk \
          sweet is sure to transport you to \
          food heaven. Whether it is pooja, \
          the festival at home or guests coming \
          home for lunch, this handy 5-minute \
          recipe is a sure blessing.",
          "imageLinks": "https://www.archanaski\
          tchen.com/images/archanas\
          kitchen/1-Author/Uma_Raghuraman/Insta\
          nt_Palkova_Recipe.jpg",
          "infoLink": "https://www.archanaski\
          tchen.com/instant-palkova-re\
          cipe-milk-based-sweet-recipe",
          "ourUser_id": 1,
          "publishedDate": "2019-02-28",
          "publisher": "Archana's Kitchen",
          "title": "Instant Palkova Recipe \
          (Milk Based Sweet Recipe)"},
         {"author": "Uma Raghuraman",
          "bookType": "Cook",
          "category_id": 4,
          "description": "ACA",
          "imageLinks": "http://4.bp.blogs\
          pot.com/-SM7Jrw1WgKk/T154EEAz\
          zyI/AAAAAAAAFF0/11p\
          IjCFAUE0/s1600/DSC06213.JPG",
          "infoLink": "https://www.archanask\
          itchen.com/instant-palkov\
          a-recipe-milk-based-sweet-recipe",
          "ourUser_id": 1,
          "publishedDate": "2019-01-01",
          "publisher": "Archana's Kitchen",
          "title": "Instant Palkova Recipe (Milk Based Sweet Recipe)"},
         {"author": "Chitra's Food Book",
          "bookType": "Cook",
          "category_id": 4,
          "description": "It's a universally loved Indian dessert recipe. I\
          n most of the Indian households, Gulab jamun recipe will be in \
          the Diwali sweets menu for sure. Many \
          people make it as the last minute \
          sweet for Diwali and other special occasions \
          like birthday, anniversary, New \
          year celebration and even for \
          Valentine’s day. Most of us opt for \
          Gulab jamun recipe using readymade, \
          store-bought Instant mix as it's \
          easy and quick to make, \
          cheap in price compared to other sweets in \
          shops. Even though the ingredients used \
          in the gulab jamun mix are the same, \
          there are many brands available in the \
          market with their own variations & style. \
          Some of the most popular ones are MTR, \
          GITS, Aachi, Bambino and Orkay. ",
          "imageLinks": "https://c2.staticfl\
          ickr.com/6/5509/30562382236_\
          0bd1f360df_z.jpg",
          "infoLink": "https://www.chitrasf\
          oodbook.com/2016/10/gulab-ja\
          mun-recipe-using-instant-mix.html",
          "ourUser_id": 1,
          "publishedDate": "2019-01-01",
          "publisher": "M T R Food Products",
          "title": "Gulab Jamun Recipe With Instant Mix"},
         {"author": "Christian Plagemann, Vasanth Mohan",
          "bookType": "Virtual Reality",
          "category_id": 8,
          "description": "Effective & Engaging Content: \
          Get started learning virtual reality development \
          through interactive content like quizzes, \
          videos, and hands-on programs. Our \
          learn-by-doing approach is the most effective \
          way to establish foundational VR developer skills. ",
          "imageLinks": "https://s3.amazona\
          ws.com/iridium-content/imag\
          es/degrees/nd105/syllabus-image.png",
          "infoLink": "https://in.udacity.com/c\
          ourse/vr-foundations-nanodegree--nd105",
          "ourUser_id": 1,
          "publishedDate": "2019-02-28",
          "publisher": "Udacity",
          "title": "VR Foundations LEARN THE \
          BASICS OF VR WITH UNITY"},
         {"author": "Hanuman",
          "bookType": "God",
          "category_id": 9,
          "description": "శ్రీ రామ రామ రామేతి రమే \
          రామే మనోరమే\nసహస్రనామ తత్తుల్యం \
          రామనామ వరాననే ...!",
          "imageLinks": "http://images.ki\
          nige.com/cover600/9200/SriRa\
          maRamamrutam600.jpg",
          "infoLink": "http://kinige.com/b\
          ook/Sri+Rama+Ramamrutam",
          "ourUser_id": 1,
          "publishedDate": "2019-02-28",
          "publisher": "Ayodhya",
          "title": "SRI RAMA"},
         {"author": "YOUR GALACTIC ADVENTURE AWAITS",
          "bookType": "Virtual Reality",
          "category_id": 8,
          "description": "EVE Online is a \
          community-driven spaceship MMO where players \
          can play for free, choosing their \
          own path from countless options. \
          Experience space exploration, immense \
          PvP and PvE battles, mining, industry \
          and a thriving player economy in an ever-\
          expanding sandbox.",
          "imageLinks": "https://web.ccpga\
          mescdn.com/aws/eveonl\
          ine/images/big-red.jpg",
          "infoLink": "https://www.eveon\
          line.com/?gclid=EAIaIQobChMIj\
          u6vuvrn4AIVzkwrCh2BtQm-EAE\
          YASAAEgLm_fD_BwE&gclsrc=aw.ds",
          "ourUser_id": 1,
          "publishedDate": "2019-01-01",
          "publisher": "EVE",
          "title": "EVE"},
         {"author": " Thomas Disch",
          "bookType": "Comics",
          "category_id": 3,
          "description": "This article is about Disney's \
          1994 animated film. For the upcoming \
          2019 remake of the same name, see The Lion \
          King (2019 film). For the franchise \
          as a whole, see The Lion King (franchise). ",
          "imageLinks": "https://www.bing.com/th?id=OIP.QG7V8\
          pxWFiZ2lYD86jay0QHaEK&pid=Api",
          "infoLink": "https://en.wikipedia.org/wiki/The\
          _Lion_King",
          "ourUser_id": 2,
          "publishedDate": "2019-03-22",
          "publisher": "Disney",
          "title": "The Lion King"}]

titles = []
for i in range(0, len(books)):
    # print(book["title"],book["author"],book["bookType"],book["description"],book["publishedDate"],book["publisher"],book["imageLinks"],book["infoLink"],book["category_id"])
    titles.append(books[i]['title'].replace(' ', ''))
    titles[i] = Books(title=books[i]["title"],
                      author=books[i]["author"],
                      bookType=books[i]["bookType"],
                      description=books[i]["description"],
                      publishedDate=books[i]["publishedDate"],
                      publisher=books[i]["publisher"],
                      imageLinks=books[i]["imageLinks"],
                      infoLink=books[i]["infoLink"],
                      category_id=books[i]["category_id"],
                      ourUser_id=books[i]["ourUser_id"])
    print(titles[i])
    session.add(titles[i])
    session.commit()
    print("Data Created...!")
