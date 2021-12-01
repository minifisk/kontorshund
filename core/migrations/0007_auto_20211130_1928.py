# Generated by Django 3.2.9 on 2021-11-30 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_advertisement_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.area', verbose_name='Område'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='breed',
            field=models.CharField(choices=[('3', 'Affenpinscher'), ('6', 'Afghanhund'), ('7', 'Africanis'), ('8', "Aidi (Chien de Montagne de l'Atlas)"), ('9', 'Ainu, seHokkaido'), ('10', 'Airedaleterrier'), ('11', 'Akbash'), ('12', 'Akita (Akita inu)'), ('13', 'Alano español'), ('14', 'Alentejomastiff, se Rafeiro do alentejo'), ('15', 'Alaskan malamute'), ('16', 'Alpenländische dachsbracke'), ('17', 'Altdeutsche Hütehunde'), ('18', 'American akita (Great japanese dog)'), ('19', 'American Bulldog'), ('20', 'American English Coonhound'), ('21', 'American eskimo dog'), ('22', 'American foxhound'), ('23', 'American hairless terrier'), ('24', 'American Leopard Hound'), ('25', 'American staffordshire terrier'), ('26', 'American toy fox terrier'), ('27', 'American water spaniel (Amerikansk vattenspaniel)'), ('28', 'Amerikansk cocker spaniel'), ('29', 'Amerikansk pitbullterrier (Pitbull Terrier)'), ('30', 'Anatolisk herdehund (Karabash), se Kangal Çoban Köpeği'), ('31', 'Anglo-français de petite vénerie'), ('32', 'Anglo-russkaja gontjaja (Rysk fläckig stövare)'), ('33', 'Appenzeller sennenhund'), ('34', 'Ariégeois'), ('35', 'Australian cattledog'), ('36', 'Australian kelpie'), ('37', 'Australian Silky Terrier, se Silky terrier'), ('38', 'Australian shepherd'), ('39', 'Australian stock dog, se Working kelpie'), ('40', 'Australian stumpy tail cattle dog'), ('41', 'Australisk terrier'), ('42', 'Azawakh'), ('43', 'Balgarski barak (Bulgarisk strävhårig stövare)'), ('44', 'Balgarsko gontje (Bulgarisk stövare)'), ('45', 'Balgarsko ovtjarsko kutje (Karakatjan)'), ('46', 'Balkanski gonic, se Serbski gonic'), ('47', 'Barbado da Terceira'), ('48', 'Barbet (Fransk vattenhund)'), ('49', 'Basenji'), ('50', 'Basset artésien normand'), ('51', 'Basset bleu de gascogne'), ('52', 'Basset fauve de bretagne'), ('53', 'Basset griffon vendéen; petit och grand'), ('54', 'Basset hound'), ('55', 'Bayersk viltspårhund'), ('56', 'Beagle'), ('57', 'Beagle-harrier'), ('58', 'Bearded collie'), ('59', 'Beauceron (Berger de Bauce)'), ('60', 'Bedlingtonterrier'), ('61', 'Belgisk vallhund; groenendael, laekenois, malinois och tervueren'), ('62', 'Bergamasco'), ('63', 'Berger blanc suisse, se Vit herdehund'), ('64', 'Berger de Bauce, se Beauceron'), ('65', 'Berger de Brie, se Briard'), ('66', 'Berger de Crau'), ('67', 'Berger des pyrénées (Pyreneisk vallhund); à poil long och à face rase'), ('68', 'Berger picard (Picardy)'), ('69', 'Berner sennenhund'), ('70', 'Bernerstövare, se Schweiziska stövare'), ('71', 'Bichon petit chien lion, se Löwchen'), ('72', 'Bichon frisé'), ('73', 'Bichon havanais (Bichon havanese)'), ('74', 'Biewer Terrier'), ('75', 'Billy'), ('76', 'Black and tan coonhound'), ('77', 'Blodhund (Engelsk blodhund)'), ('78', 'Blue Lacy'), ('79', 'Bluetick coonhound'), ('80', 'Boerboel'), ('81', 'Bolognese'), ('82', 'Bolonka, se Russkaja tsvetnaja bolonka'), ('83', 'Border collie'), ('84', 'Borderterrier'), ('85', 'Borzoi (Rysk vinthund)'), ('86', 'Bosanski ostrodlaki gonic-barak'), ('87', 'Bostonterrier'), ('88', 'Bordeauxdogg, se Dogue de bordeaux'), ('89', 'Bouvier des ardennes'), ('90', 'Bouvier des flandres'), ('91', 'Boxer'), ('92', 'Boykin Spaniel'), ('93', 'Bracco italiano (Italiensk pointer)'), ('94', 'Brandlbracke (vieräugl)'), ('95', "Braque d'auvergne"), ('96', 'Braque de l’ariège'), ('97', 'Braque du bourbonnais'), ('98', 'Braque dupuy (Braque du Puy)'), ('99', 'Braque français; type gascogne och type pyrénées'), ('100', 'Braque saint-germain'), ('101', 'Breton'), ('102', 'Briard (Berger de Brie)'), ('103', 'Briquet de Provence'), ('104', 'Briquet griffon vendéen'), ('105', 'Broholmer'), ('106', 'Bruno Saint Hubert français'), ('107', 'Buldogue campeiro'), ('108', 'Buldogue serrano'), ('109', 'Bull Dog, se Engelsk bulldogg'), ('110', 'Bullenbeisser (utdöd)'), ('111', 'Bullmastiff'), ('112', 'Bullterrier'), ('113', 'Burjat-mongolskij volkodav (Burjatvarghund)'), ('114', 'Böhmisk vallhund, se Chodský pes'), ('115', 'Ca de bestiar (Perro de pastor mallorquín)'), ('116', 'Ca de bou, se Perro dogo mallorquin'), ('117', 'Cairnterrier'), ('118', 'Canaan dog'), ('119', 'Canadian eskimo dog'), ('120', 'Cane corso'), ('121', 'Cane da pastore Bergamasco, se Bergamasco'), ('122', 'Cão da serra da estrela'), ('123', 'Cão da serra de aires'), ('124', 'Cão de castro laboreiro'), ('125', 'Cão de gado transmontano'), ('126', 'Cão fila de são miguel'), ('127', 'Caravan Hound'), ('128', 'Carea leonés (Perro leonés de pastor)'), ('129', 'Carolina Dog'), ('130', 'Catahoula Leopard Dog'), ('131', 'Cavalier king charles spaniel'), ('132', 'Cesky fousek'), ('133', 'Český horský pes'), ('134', 'Český strakatý pes'), ('135', 'Ceskyterrier'), ('136', 'Ceskoslovenský vlciak (Tjeckoslovakisk varghund)'), ('137', 'Chart polski'), ('138', 'Chesapeake bay retriever'), ('139', 'Chien Corse, se Cursinu'), ('140', 'Chien d’artois'), ('141', "Chien de Montagne de l'Atlas, se Aidi"), ('142', 'Chien gris de Saint Louis (utdöd)'), ('143', 'Chihuahua; kort- och långhårig'), ('144', 'Chinese crested dog (Kinesisk nakenhund); hairless och powder puff'), ('145', 'Chinook'), ('146', 'Chippiparai'), ('147', 'Chodský pes (Böhmisk vallhund)'), ('148', 'Chortaj'), ('149', 'Chow chow'), ('150', 'Ciobanesc romanesc carpatin'), ('151', 'Ciobanesc romanesc corb'), ('152', 'Ciobanesc romanesc de bucovina'), ('153', 'Ciobanesc romanesc mioritic'), ('154', 'Cimarrón uruguayo'), ('155', "Cirneco dell'etna"), ('156', 'Clumber spaniel'), ('157', 'Coban Köpegi, se Anatolisk herdehund'), ('158', 'Cocker spaniel (Engelsk cocker spaniel)'), ('159', 'Collie; kort- och långhårig'), ('160', 'Combai (Kombai)'), ('161', 'Coton de tuléar'), ('162', 'Crnogorski planinski gonic'), ('163', 'Curly coated retriever'), ('164', 'Cursinu (Chien Corse)'), ('165', 'Czeslovakian Wolfdog, se Ceskoslovenský vlciak'), ('166', 'Dalbohund (utdöd)'), ('167', 'Dalmatiner'), ('168', 'Dandie dinmont terrier'), ('169', 'Dansk spids'), ('170', 'Dansk-svensk gårdshund'), ('171', 'Deutsch Drahthaar, se Strävhårig vorsteh'), ('172', 'Deutsch Kurzhaar, se Korthårig vorsteh'), ('173', 'Deutsch Langhaar, se Långhårig vorsteh'), ('174', 'Deutsch stichelhaar (Stichelhaariger deutscher vorsteh)'), ('175', 'Deutsche bracke'), ('176', 'Deutsche Dogge, se Grand danois'), ('177', 'Deutscher Jagdterrier, se Tysk jaktterrier'), ('178', 'Deutscher Pinscher, se Pinscher'), ('179', 'Dhokhi apso, se Tibetansk terrier'), ('180', 'Dingo'), ('181', 'Dobermann'), ('182', 'Dogo argentino'), ('183', 'Dogo canario'), ('184', 'Dogo guatemalteco'), ('185', 'Dogue brasileiro'), ('186', 'Dogue de bordeaux (Bordeauxdogg)'), ('187', 'Do-Khyi, se Tibetansk mastiff'), ('188', 'Drentsche patrijshond'), ('189', 'Drever'), ('190', 'Dunkerstövare'), ('191', 'Dvärgpinscher'), ('192', 'Dvärgpudel, se Pudel'), ('193', 'Dvärgschnauzer'), ('194', 'Dvärgspets, se Pomeranian'), ('195', 'Dvärgtax, se Tax; kort-, lång- och strävhårig'), ('196', 'Engelsk blodhund, se Blodhund'), ('197', 'Engelsk bulldogg (Bull Dog)'), ('198', 'Engelsk cocker spaniel, se Cocker spaniel'), ('199', 'Engelsk foxhound, se Foxhound'), ('200', 'Engelsk setter'), ('201', 'Engelsk springer spaniel'), ('202', 'English Coonhound (Redtick Coonhound), se American English Coonhound'), ('203', 'English toy terrier'), ('204', 'Entlebucher sennenhund'), ('205', 'Épagneul Barbet, se Barbet'), ('206', 'Épagneul bleu de picardie'), ('207', 'Épagneul Breton, se Breton'), ('208', 'Épagneul de pont-audemer'), ('209', 'Épagneul de saint usuge'), ('210', 'Épagneul français'), ('211', 'Épagneul picard'), ('212', 'Erdélyi kopó'), ('213', 'Estnisk stövare (Eesti hagijas)'), ('214', 'Eurasier'), ('215', 'Euskal Artzain Txakurra, se Perro de Pastor Vasco'), ('216', 'Faraohund (Kelbtal Fenek)'), ('217', 'Field spaniel'), ('218', 'Fila brasileiro'), ('219', 'Finsk lapphund (Lapinkoira)'), ('220', 'Finsk spets'), ('221', 'Finsk stövare'), ('222', 'Flat coated retriever'), ('223', 'Foxhound'), ('224', 'Foxterrier; släthårig och strävhårig'), ('225', 'Français blanc et noir'), ('226', 'Français blanc et orange'), ('227', 'Français tricolore'), ('228', 'Fransk bulldogg'), ('229', 'Fransk vattenspaniel / Fransk vattenhund, se Barbet'), ('230', 'Frisisk vattenhund, se Wetterhoun'), ('231', 'Galgo español'), ('232', 'Gammel dansk hönsehund'), ('233', 'Gampr'), ('234', 'Gascon saintongeois, grand och petit'), ('235', 'Golden retriever'), ('236', 'Gonczy polski'), ('237', 'Gordonsetter'), ('238', "Gos d'atura catalá (Perro de pastor catalán, Katalansk vallhund)"), ('239', 'Gos Rater Valencià, se Ratonero Valenciano'), ('240', 'Gotlandsstövare'), ('241', 'Grand anglo-français blanc et noir'), ('242', 'Grand anglo-français blanc et orange'), ('243', 'Grand anglo-français tricolore'), ('244', 'Grand basset griffon vendéen'), ('245', 'Grand bleu de gascogne'), ('246', 'Grand danois (Deutsche Dogge)'), ('247', 'Grand gascon saintongeois, se Gascon saintongeois'), ('248', 'Grand griffon vendéen'), ('249', 'Great japanese dog, se American akita'), ('250', 'Greyhound'), ('251', 'Griffon à poil laineux (Griffon Boulet)'), ('252', 'Griffon belge'), ('253', 'Griffon bleu de gascogne'), ('254', 'Griffon bruxellois'), ('255', "Griffon d'arret à poil dur (korthals)"), ('256', 'Griffon fauve de bretagne'), ('257', 'Griffon nivernais'), ('258', 'Groenendael, se Belgisk vallhund'), ('259', 'Grosser münsterländer'), ('260', 'Grosser schweizer sennenhund'), ('261', 'Grosspitz (Tysk spets / Grosspitz)'), ('262', 'Gråhund, se Norsk älghund, grå'), ('263', 'Grönlandshund'), ('264', 'Haldenstövare'), ('265', 'Hamiltonstövare'), ('266', 'Hannoveransk viltspårhund'), ('267', 'Harrier'), ('268', 'Hedehund'), ('269', 'Hellinikos ichnilatis'), ('270', 'Hellinikos poimenikos (Grekisk herdehund)'), ('271', 'Hokkaido (Ainu)'), ('272', 'Hollandse herdershond (Holländsk vallhund); korthårig, långhårig och strävhårig'), ('273', 'Hollandse smoushond'), ('274', 'Hovawart'), ('275', 'Hrvatski ovcar'), ('276', 'Hygenstövare (Hygenhund)'), ('277', 'Hälleforshund'), ('278', 'Irish glen of imaal terrier'), ('279', 'Irish softcoated wheaten terrier'), ('280', 'Irländsk röd och vit setter'), ('281', 'Irländsk röd setter'), ('282', 'Irländsk terrier'), ('283', 'Irländsk varghund'), ('284', 'Irländsk vattenspaniel'), ('285', 'Isländsk fårhund'), ('286', 'Istarski gonic (Istrian hound); kratkodlaki och ostrodlaki'), ('287', 'Italiensk pointer, se Bracco italiano'), ('288', 'Italiensk vinthund'), ('289', 'Jack russell terrier'), ('290', 'Jakutskaja lajka'), ('291', 'Japanese chin'), ('292', 'Japansk spets'), ('293', 'Japansk terrier, se Nihon teria'), ('294', 'Jemtse apso, se Tibetansk spaniel'), ('295', 'Jugoslovenski Ovcarski Pas, se Sarplaninac'), ('296', 'Jurastövare, se Schweiziska stövare'), ('297', 'Juzjnorusskaja ovtjarka (Sydrysk ovtjarka)'), ('298', 'Jämthund'), ('299', 'Kai (Kai ken)'), ('300', 'Kangal Çoban Köpeği (Anatolisk herdehund / Karabash)'), ('301', 'Kanintax, se Tax; kort-, lång- och strävhårig'), ('302', 'Karabash, se (Karabash)'), ('303', 'Karakatjan, se Balgarsko ovtjarsko kutje'), ('304', 'Karelsk björnhund'), ('305', "Katalansk vallhund, se Gos d'atura catalá"), ('306', 'Kaukasisk ovtjarka, se Kavkazskaja ovtjarka'), ('307', 'Kavkazskaja ovtjarka (Kaukasisk ovtjarka)'), ('308', 'Keeshond (Tysk spets / Wolfspitz)'), ('309', 'Kelpie, se Australian kelpie'), ('310', 'Kerry Beagle'), ('311', 'Kerry blue terrier'), ('312', 'Kinesisk nakenhund, Chinese crested dog'), ('313', 'King charles spaniel'), ('314', 'Kintamani-Balihund'), ('315', 'Kishu'), ('316', 'Kleiner münsterländer'), ('317', 'Kleinspitz (Tysk spets / Kleinspitz)'), ('318', 'Kokoni'), ('319', 'Kombai, se Combai'), ('320', 'Komondor'), ('321', 'Kooikerhondje, se Nederlandse kooikerhondje'), ('322', 'Kopó (Transsylvansk kopó), se Erdélyi kopó'), ('323', 'Korea jindo dog'), ('324', "Korthals, se Griffon d'arret à poil dur"), ('325', 'Korthårig vorsteh (Deutsch Kurzhaar)'), ('326', 'Kraski ovcar'), ('327', 'Kritikos lagonikos (Kretahund)'), ('328', 'Kromfohrländer'), ('329', 'Kunming langgou (Kunmingvarghund)'), ('330', 'Kuvasz'), ('331', 'Labrador retriever'), ('332', 'Lagotto romagnolo'), ('333', 'Lakelandterrier'), ('334', 'Lakenois, se Belgisk vallhund'), ('335', 'Lajka, se Rysk-europeisk lajka, Västsibirisk lajka och Östsibirisk'), ('336', 'Lancashire heeler'), ('337', 'Landseer'), ('338', 'Lapphund, se Finsk lapphund och Svensk lapphund'), ('339', 'Lapsk vallhund (Lapinporokoira)'), ('340', 'Leiko helliniko tsopanoskilo (Vit grekisk herdehund)'), ('341', 'Leonberger'), ('342', 'Lhasa apso'), ('343', 'Lietuviu skalikas (Litauisk stövare)'), ('344', 'Lupo italiano'), ('345', 'Luzernerstövare, se Schweiziska stövare'), ('346', 'Långhårig vorsteh (Deutsch Langhaar)'), ('347', 'Löwchen (Bichon petit chien lion)'), ('348', 'Magyar agár (Ungersk vinthund)'), ('349', 'Majorero'), ('350', 'Mali medimurski pas (Medi)'), ('351', 'Malinois, se Belgisk vallhund'), ('352', 'Mallorcamastiff, se Perro dogo mallorquín'), ('353', 'Malteser'), ('354', 'Manchesterterrier'), ('355', 'Maneto'), ('356', 'Maremmano abruzzese (Maremma)'), ('357', 'Markiesje'), ('358', 'Mastiff'), ('359', 'Mastín del Pirineo, se Pyreneisk mastiff'), ('360', 'Mastin español (Spansk mastiff)'), ('361', 'Mastino napoletano (Neapolitansk mastiff)'), ('362', 'Mâtin Belge'), ('363', 'Mellanasiatisk ovtjarka, se Sredneasiatskaja ovtjarka'), ('364', 'Mellanpinscher, se Pinscher'), ('365', 'Mellanpudel, se Pudel'), ('366', 'Mellanschnauzer, se Schnauzer'), ('367', 'Mexikansk nakenhund, se Xoloitzcuintle'), ('368', 'Miniatyrbullterrier'), ('369', 'Miniature american shepherd'), ('370', 'Mittelspitz (Tysk spets / Mittelspitz)'), ('371', 'Molossos tis Ipeiro (Epirusmoloss)'), ('372', 'Mops'), ('373', 'Moskovskaja storozjevaja (Moskvavakthund)'), ('374', 'Moskvadvärgterrier, se Russkiy toy'), ('375', 'Mountain Cur'), ('376', 'Mudhol, se Caravan Hound'), ('377', 'Mudi'), ('378', 'Münsterländer; (kleiner münsterländer och grosser münsterländer'), ('379', 'Neapolitansk mastiff, se Mastino napoletano'), ('380', 'Nederlandse kooikerhondje'), ('381', 'Nenetskaja olenegonka lajka, se Olenegonka sjpits'), ('382', 'Newfoundlandshund'), ('383', 'Nihon teria (Japansk terrier)'), ('384', 'Norfolkterrier'), ('385', 'Norrbottenspets'), ('386', 'Norsk buhund'), ('387', 'Norsk lundehund'), ('388', 'Norsk älghund, grå (Gråhund)'), ('389', 'Norsk älghund, svart'), ('390', 'Norwichterrier'), ('391', 'Nova scotia duck tolling retriever'), ('392', 'Nya Guineas sjungande hund'), ('393', 'Olde english bulldogge brasileiro'), ('394', 'Ogar polski'), ('395', 'Ohar, se Slovenský hrubosrsty stavac'), ('396', 'Old english sheepdog'), ('397', 'Olenegonnyj sjpits (Nenetskaja olenegonka lajka, Nenetsrenhund)'), ('398', 'Otterhound (Utterhund)'), ('399', 'Ovejero magallánico'), ('400', 'Ovelheiro gaúcho'), ('401', 'Pachón navarro'), ('402', 'Papillon'), ('403', 'Parson russell terrier'), ('404', 'Pashmi, se Caravan Hound'), ('405', 'Pekingese'), ('406', 'Perdiguero de burgos'), ('407', 'Perdigueiro português'), ('408', 'Perro de agua español (Spansk vattenhund)'), ('409', "Perro de pastor catalán, se Gos d'atura catalá"), ('410', 'Perro de pastor garafiano'), ('411', 'Perro de pastor mallorquín, se Ca de bestiar'), ('412', 'Perro de pastor vasco (Euskal Artzain Txakurra)'), ('413', 'Perro dogo mallorquín (Ca de bou, Mallorcamastiff)'), ('414', 'Perro leonés de pastor, se Carea leonés'), ('415', 'Perro sin pelo del perú (Peruansk nakenhund); liten, mellan och stor'), ('416', 'Peruansk nakenhund, se Perro sin pelo de perú'), ('417', 'Petit basset griffon vendéen'), ('418', 'Petit bleu de gascogne'), ('419', 'Petit gascon saintongeois, se Gascon saintongeois'), ('420', 'Petit brabancon'), ('421', 'Phaléne'), ('422', 'Picardy, se Berger picard'), ('423', 'Pinscher'), ('424', 'Pitbull Terrier (se Amerikansk pitbullterrier)'), ('425', 'Plott'), ('426', 'Podenco andaluz'), ('427', 'Podenco canario'), ('428', 'Podenco ibicenco, korthårig och strävhårig'), ('429', 'Podenco valenciano'), ('430', 'Podengo portugues, cerdoso och liso'), ('431', 'Pointer'), ('432', 'Poitevin'), ('433', 'Polski owczarek nizinny'), ('434', 'Polski owczarek podhalanski'), ('435', 'Pomeranian (Tysk spets / Zwergspitz, Dvärgspets)'), ('436', 'Porcelaine'), ('437', 'Portugisisk vattenhund (Cão de agua portugués)'), ('438', 'Posavski gonic'), ('439', 'Prazský krysarík'), ('440', 'Pudel'), ('441', 'Pudelpointer'), ('442', 'Puli'), ('443', 'Pumi'), ('444', 'Pyrenéerhund'), ('445', 'Pyreneisk mastiff'), ('446', 'Pyreneisk vallhund, se Berger des pyrénées'), ('447', 'Rafeiro do alentejo (Alentejomastiff)'), ('448', 'Rajapalayam'), ('449', 'Rampur Hound'), ('450', 'Rastreador brasileiro'), ('451', 'Ratonero bodeguero andaluz'), ('452', 'Ratonero valenciano (Gos rater valencià)'), ('453', 'Rat terrier'), ('454', 'Redbone Coonhound'), ('455', 'Redtick Coonhound, se American English Coonhound'), ('456', 'Rhodesian ridgeback'), ('457', 'Riesenschnauzer'), ('458', 'Rottweiler'), ('459', 'Russkaja gontjaja (Rysk stövare)'), ('460', 'Russkaja ochotnitjija spaniel (Rysk jaktspaniel)'), ('461', 'Russkaja pegaja gontjaja, se Anglo-russkaja gontjaja'), ('462', 'Russkaja tsvetnaja bolonka'), ('463', 'Russkiy toy (Moskvadvärgterrier)'), ('464', 'Rysk-europeisk lajka'), ('465', 'Rysk fläckig stövare, se Anglo-russkaja gontjaja'), ('466', 'Rysk stövare, se Russkaja gontjaja'), ('467', 'Rysk svart terrier (Tjornyj terjer)'), ('468', 'Rysk vinthund, se Borzoi'), ('469', 'Saarloos wolfhond'), ('470', 'Sabueso español'), ('471', 'Saluki'), ('472', 'Samojedhund'), ('473', "St. John's Dog (utdöd)"), ('474', 'Sankt bernhardshund; kort- och långhårig'), ('475', 'Sarplaninac (Jugoslovenski ovcarski pas)'), ('476', 'Schafpudel'), ('477', 'Schapendoes'), ('478', 'Schillerstövare'), ('479', 'Schipperke'), ('480', 'Schnauzer (Mellanschnauzer)'), ('481', 'Schweizer sennenhund, se Grosser schweizer sennenhund'), ('482', 'Schweiziska små stövare; berner, jura, luzerner och schwyzer'), ('483', 'Schweiziska stövare; berner, jura, luzerner och schwyzer'), ('484', 'Schwyzerstövare, se Schweiziska stövare'), ('485', 'Schäfer, se Tysk schäferhund'), ('486', 'Sealyhamterrier'), ('487', "Segugio dell'Appennino"), ('488', 'Segugio italiano, korthårig eller strävhårig'), ('489', 'Segugio maremmano, korthårig eller strävhårig'), ('490', 'Serbski gonic (Balkanski gonic)'), ('491', 'Serbski trobojni gonic'), ('492', 'Shar pei'), ('493', 'Shetland sheepdog'), ('494', 'Shiba'), ('495', 'Shih tzu'), ('496', 'Shikoku'), ('497', 'Siberian husky'), ('498', 'Silken Windhound'), ('499', 'Silkyterrier (Australian Silky Terrier)'), ('500', 'Skotsk hjorthund'), ('501', 'Skotsk terrier'), ('502', 'Skyeterrier'), ('503', 'Sloughi'), ('504', 'Slovenský cuvac'), ('505', 'Slovenský hrubosrsty stavac (Ohar)'), ('506', 'Slovenský kopov'), ('507', 'Släthårig foxterrier'), ('508', 'Smålandsstövare'), ('509', 'Spansk mastiff, se Mastin español'), ('510', 'Spansk vattenhund, se Perro de agua español'), ('511', 'Spinone'), ('512', 'Sredneasiatskaja ovtjarka (Mellanasiatisk ovtjarka)'), ('513', 'Srpski pastirski pas (Serbisk herdehund)'), ('514', 'Stabijhoun'), ('515', 'Staffordshire bullterrier'), ('516', 'Steirische rauhhaarbracke'), ('517', 'Stichelhaariger deutscher vorsteh, se Deutsch stichelhaar'), ('518', 'Storpudel, se Pudel'), ('519', 'Strellufstövare, se Drever'), ('520', 'Strävhårig foxterrier'), ('521', 'Strävhårig vorsteh (Deutsch Drahthaar)'), ('522', 'Sulimovhund'), ('523', 'Sussex spaniel'), ('524', 'Svart terrier, se Rysk svart terrier'), ('525', 'Svensk lapphund'), ('526', 'Svensk vit älghund'), ('527', 'Sydrysk ovtjarka, se Juzjnorusskaja ovtjarka'), ('528', 'Taigan[1]'), ('529', 'Taiwan dog'), ('530', 'Tax; kort-, lång- och strävhårig'), ('531', 'Teddy Roosevelt Terrier'), ('532', 'Tenterfield terrier'), ('533', 'Terrier brasileiro'), ('534', 'Terrier chileno'), ('535', 'Tervueren, se Belgisk vallhund'), ('536', 'Thai bangkaew dog'), ('537', 'Thai ridgeback dog'), ('538', 'Tibetansk mastiff (Do-Khyi)'), ('539', 'Tibetansk spaniel'), ('540', 'Tibetansk terrier (Dhokhi apso)'), ('541', 'Tirolerbracke'), ('542', 'Tjornyj terjer, se Svart terrier'), ('543', 'Tjukotskaja jesdovaja'), ('544', 'Tornjak'), ('545', 'Tosa (Tosa inu)'), ('546', 'Toy Fox Terrier, se American toy fox terrier'), ('547', 'Toypudel, se Pudel'), ('548', 'Transsylvansk kopó, se Erdélyi kopó'), ('549', 'Treeing Tennessee Brindle'), ('550', 'Treeing walker coonhound'), ('551', 'Tweed Water Spaniel (utdöd)'), ('552', 'Tysk jaktterrier (Deutscher Jagdterrier)'), ('553', 'Tysk schäferhund; normalhårig och långhårig'), ('554', 'Tysk spets; grosspitz, kleinspitz, mittelspitz, keeshond (wolfspitz) och pomeranian (zwergspitz / dvärgspets)'), ('555', 'Ungersk vinthund, se Magyar agár'), ('556', 'Ungersk viszla, kort- och strävhårig'), ('557', 'Utterhund, se Otterhound'), ('558', 'Veadeiro pampeano'), ('559', 'Vit herdehund (Berger blanc suisse)'), ('560', 'Volpino italiano'), ('561', 'Vorsteh; kort- (Deutsch Kurzhaar), lång- (Deutsch Langhaar) och strävhårig (Deutsch Drahthaar)'), ('562', 'Vostotjnoevropejskaja ovtjarka (Östeuropeisk ovtjarka)'), ('563', 'Västgötaspets'), ('564', 'Västsibirisk lajka'), ('565', 'Wachtelhund'), ('566', 'Weimaraner'), ('567', 'Welsh corgi cardigan'), ('568', 'Welsh corgi pembroke'), ('569', 'Welsh springer spaniel'), ('570', 'Welshterrier'), ('571', 'West highland white terrier'), ('572', 'Westfälische dachsbracke'), ('573', 'Wetterhoun (Frisisk vattenhund)'), ('574', 'Whippet'), ('575', 'Viszla, se Ungersk vizsla'), ('576', 'Wolfspitz, se Keeshond'), ('577', 'Working kelpie'), ('578', 'Xoloitzcuintle (Mexikansk nakenhund); liten, mellan och stor'), ('579', 'Yorkshireterrier'), ('580', 'Zwergspitz, se Pomeranian'), ('581', 'Österreichischer pinscher (Österreichischer kurzhaariger pinscher)'), ('582', 'Östsibirisk lajka')], default=3, max_length=3, verbose_name='Ras'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='days_per_week',
            field=models.CharField(choices=[('1', '1 day per week'), ('1-5', '1-2 days per week'), ('1-3', '1-3 days per week'), ('1-4', '1-4 days per week'), ('1-5', '1-5 days per week')], default=1, max_length=3, verbose_name='Dagar per vecka'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Beskrivning'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='municipality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.municipality', verbose_name='Kommun'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default='S', max_length=2, verbose_name='Storlek'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Titel'),
        ),
    ]
