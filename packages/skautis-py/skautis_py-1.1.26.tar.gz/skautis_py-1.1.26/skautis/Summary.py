# -*- coding: utf-8 -*-

import zeep

# Exporty/přehledy
class Summary(object):
    __module__ = 'skautis'

    def __init__(self, test):
        if test:
            self._client = zeep.Client('https://test-is.skaut.cz/JunakWebservice/Summary.asmx?wsdl')
        else:
            self._client = zeep.Client('https://is.skaut.cz/JunakWebservice/Summary.asmx?wsdl')

    # Načíst seznam typů jednotky pro export osob
    def ExportUnitUnitTypeAll(self, ID_Login, ID_ExportUnit, ID, ID_UnitType=None):
        return self._client.service.ExportUnitUnitTypeAll({"ID_Login": ID_Login, "ID_ExportUnit": ID_ExportUnit, "ID": ID, "ID_UnitType": ID_UnitType})

    # Zobrazit export jednotek
    def ExportUnitView(self, ID_Login, ID, ID_UnitFilter):
        return self._client.service.ExportUnitView({"ID_Login": ID_Login, "ID": ID, "ID_UnitFilter": ID_UnitFilter})

    # Načíst seznam šablon exportu jednotek
    def ExportUnitAll(self, ID_Login, ID, DisplayName=None):
        return self._client.service.ExportUnitAll({"ID_Login": ID_Login, "ID": ID, "DisplayName": DisplayName})

    # Smazat šablonu exportu jednotek
    def ExportUnitDelete(self, ID_Login, ID):
        return self._client.service.ExportUnitDelete({"ID_Login": ID_Login, "ID": ID})

    # Načíst detail šablony exportu jednotek
    def ExportUnitDetail(self, ID_Login, ID):
        return self._client.service.ExportUnitDetail({"ID_Login": ID_Login, "ID": ID})

    # Kopie šablonu exportu jednotek
    def ExportUnitClone(self, ID_Login, ID, ID_Person, RegistrationYear, Contact, AligmentType, Leaders, Location, Address, ViewDisplayName, RegistrationNumber, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, IC, DIC, ID_UnitFilter, TroopArt, MemberCount, UnitType, FilterAligmentType, FilterTroopArt, FilterUnitType, IsPublic, Person=None, DisplayName=None, AlignmentTypes=None, TroopArts=None, ContactTypes=None, UnitTypes=None):
        return self._client.service.ExportUnitClone({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "Contact": Contact, "AligmentType": AligmentType, "Leaders": Leaders, "Location": Location, "Address": Address, "ViewDisplayName": ViewDisplayName, "RegistrationNumber": RegistrationNumber, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "IC": IC, "DIC": DIC, "ID_UnitFilter": ID_UnitFilter, "TroopArt": TroopArt, "MemberCount": MemberCount, "UnitType": UnitType, "FilterAligmentType": FilterAligmentType, "FilterTroopArt": FilterTroopArt, "FilterUnitType": FilterUnitType, "IsPublic": IsPublic, "Person": Person, "DisplayName": DisplayName, "AlignmentTypes": AlignmentTypes, "TroopArts": TroopArts, "ContactTypes": ContactTypes, "UnitTypes": UnitTypes})

    # Založit šablonu exportu jednotek
    def ExportUnitInsert(self, ID_Login, ID, ID_Person, RegistrationYear, Contact, AligmentType, Leaders, Location, Address, ViewDisplayName, RegistrationNumber, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, IC, DIC, ID_UnitFilter, TroopArt, MemberCount, UnitType, FilterAligmentType, FilterTroopArt, FilterUnitType, IsPublic, Person=None, DisplayName=None, AlignmentTypes=None, TroopArts=None, ContactTypes=None, UnitTypes=None):
        return self._client.service.ExportUnitInsert({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "Contact": Contact, "AligmentType": AligmentType, "Leaders": Leaders, "Location": Location, "Address": Address, "ViewDisplayName": ViewDisplayName, "RegistrationNumber": RegistrationNumber, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "IC": IC, "DIC": DIC, "ID_UnitFilter": ID_UnitFilter, "TroopArt": TroopArt, "MemberCount": MemberCount, "UnitType": UnitType, "FilterAligmentType": FilterAligmentType, "FilterTroopArt": FilterTroopArt, "FilterUnitType": FilterUnitType, "IsPublic": IsPublic, "Person": Person, "DisplayName": DisplayName, "AlignmentTypes": AlignmentTypes, "TroopArts": TroopArts, "ContactTypes": ContactTypes, "UnitTypes": UnitTypes})

    # Upravit šablonu exportu jednotek
    def ExportUnitUpdate(self, ID_Login, ID, ID_Person, RegistrationYear, Contact, AligmentType, Leaders, Location, Address, ViewDisplayName, RegistrationNumber, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, IC, DIC, ID_UnitFilter, TroopArt, MemberCount, UnitType, FilterAligmentType, FilterTroopArt, FilterUnitType, IsPublic, Person=None, DisplayName=None, AlignmentTypes=None, TroopArts=None, ContactTypes=None, UnitTypes=None):
        return self._client.service.ExportUnitUpdate({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "Contact": Contact, "AligmentType": AligmentType, "Leaders": Leaders, "Location": Location, "Address": Address, "ViewDisplayName": ViewDisplayName, "RegistrationNumber": RegistrationNumber, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "IC": IC, "DIC": DIC, "ID_UnitFilter": ID_UnitFilter, "TroopArt": TroopArt, "MemberCount": MemberCount, "UnitType": UnitType, "FilterAligmentType": FilterAligmentType, "FilterTroopArt": FilterTroopArt, "FilterUnitType": FilterUnitType, "IsPublic": IsPublic, "Person": Person, "DisplayName": DisplayName, "AlignmentTypes": AlignmentTypes, "TroopArts": TroopArts, "ContactTypes": ContactTypes, "UnitTypes": UnitTypes})

    # Zobrazit export osob
    def ExportPersonView(self, ID_Login, ID, Units=None):
        return self._client.service.ExportPersonView({"ID_Login": ID_Login, "ID": ID, "Units": Units})

    # Kopie šablony exportu osob
    def ExportPersonClone(self, ID_Login, ID, ID_Person, RegistrationYear, FunctionFilter, FunctionAnd, QualificationAnd, AgeFrom, AgeTo, ViewDisplayName, FirstName, LastName, NickName, MaidenName, Birthday, IdentificationNumber, IdentificationNumberStart, Age, Sex, IsForeign, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, Assurance, AssuranceCard, Allergy, FoodRestrictions, Drugs, SpecialRequirements, HealthLimitation, BodySkills, FunctionOneColumn, QualificationOneColumn, Membership, MembershipCategory, MembershipOneColumn, Username, Catalog, Journal, JournalRegistration, JournalAttachment, IsPublic, ParentNote, Note, RegistrationNumber, YearFrom, IsUnitEnroll, UnitEnrollCondition, AllowDataStorage, AllowAudiovisual, AllowSocialNetwork, AllowMarketing, School, IdCardValidTo, IdCardNumber, ParentFatherFirstName, ParentFatherLastName, ParentFatherPhone, ParentFatherMail, ParentFatherNote, ParentMotherFirstName, ParentMotherLastName, ParentMotherMail, ParentMotherPhone, ParentMotherNote, ParentOtherFirstName, ParentOtherLastName, ParentOtherMail, ParentOtherPhone, ParentOtherNote, ParentOtherParentType, PromiseChild, PromiseScout, PromiseOfficial, TrailProgress, Person=None, DisplayName=None, Units=None, MembershipTypes=None, RegistrationMemberships=None, MembershipCategories=None, Functions=None, Qualifications=None, ViewContactTypes=None, ViewFunctions=None, ViewQualifications=None):
        return self._client.service.ExportPersonClone({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "FunctionFilter": FunctionFilter, "FunctionAnd": FunctionAnd, "QualificationAnd": QualificationAnd, "AgeFrom": AgeFrom, "AgeTo": AgeTo, "ViewDisplayName": ViewDisplayName, "FirstName": FirstName, "LastName": LastName, "NickName": NickName, "MaidenName": MaidenName, "Birthday": Birthday, "IdentificationNumber": IdentificationNumber, "IdentificationNumberStart": IdentificationNumberStart, "Age": Age, "Sex": Sex, "IsForeign": IsForeign, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "Assurance": Assurance, "AssuranceCard": AssuranceCard, "Allergy": Allergy, "FoodRestrictions": FoodRestrictions, "Drugs": Drugs, "SpecialRequirements": SpecialRequirements, "HealthLimitation": HealthLimitation, "BodySkills": BodySkills, "FunctionOneColumn": FunctionOneColumn, "QualificationOneColumn": QualificationOneColumn, "Membership": Membership, "MembershipCategory": MembershipCategory, "MembershipOneColumn": MembershipOneColumn, "Username": Username, "Catalog": Catalog, "Journal": Journal, "JournalRegistration": JournalRegistration, "JournalAttachment": JournalAttachment, "IsPublic": IsPublic, "ParentNote": ParentNote, "Note": Note, "RegistrationNumber": RegistrationNumber, "YearFrom": YearFrom, "IsUnitEnroll": IsUnitEnroll, "UnitEnrollCondition": UnitEnrollCondition, "AllowDataStorage": AllowDataStorage, "AllowAudiovisual": AllowAudiovisual, "AllowSocialNetwork": AllowSocialNetwork, "AllowMarketing": AllowMarketing, "School": School, "IdCardValidTo": IdCardValidTo, "IdCardNumber": IdCardNumber, "ParentFatherFirstName": ParentFatherFirstName, "ParentFatherLastName": ParentFatherLastName, "ParentFatherPhone": ParentFatherPhone, "ParentFatherMail": ParentFatherMail, "ParentFatherNote": ParentFatherNote, "ParentMotherFirstName": ParentMotherFirstName, "ParentMotherLastName": ParentMotherLastName, "ParentMotherMail": ParentMotherMail, "ParentMotherPhone": ParentMotherPhone, "ParentMotherNote": ParentMotherNote, "ParentOtherFirstName": ParentOtherFirstName, "ParentOtherLastName": ParentOtherLastName, "ParentOtherMail": ParentOtherMail, "ParentOtherPhone": ParentOtherPhone, "ParentOtherNote": ParentOtherNote, "ParentOtherParentType": ParentOtherParentType, "PromiseChild": PromiseChild, "PromiseScout": PromiseScout, "PromiseOfficial": PromiseOfficial, "TrailProgress": TrailProgress, "Person": Person, "DisplayName": DisplayName, "Units": Units, "MembershipTypes": MembershipTypes, "RegistrationMemberships": RegistrationMemberships, "MembershipCategories": MembershipCategories, "Functions": Functions, "Qualifications": Qualifications, "ViewContactTypes": ViewContactTypes, "ViewFunctions": ViewFunctions, "ViewQualifications": ViewQualifications})

    # Načíst seznam šablon exportu osob
    def ExportPersonAll(self, ID_Login, DisplayName=None):
        return self._client.service.ExportPersonAll({"ID_Login": ID_Login, "DisplayName": DisplayName})

    # Smazat šablonu exportu osob
    def ExportPersonDelete(self, ID_Login, ID):
        return self._client.service.ExportPersonDelete({"ID_Login": ID_Login, "ID": ID})

    # Načíst detail šablony exportu osob
    def ExportPersonDetail(self, ID_Login, ID):
        return self._client.service.ExportPersonDetail({"ID_Login": ID_Login, "ID": ID})

    # Založit šablonu exportu osob
    def ExportPersonInsert(self, ID_Login, ID, ID_Person, RegistrationYear, FunctionFilter, FunctionAnd, QualificationAnd, AgeFrom, AgeTo, ViewDisplayName, FirstName, LastName, NickName, MaidenName, Birthday, IdentificationNumber, IdentificationNumberStart, Age, Sex, IsForeign, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, Assurance, AssuranceCard, Allergy, FoodRestrictions, Drugs, SpecialRequirements, HealthLimitation, BodySkills, FunctionOneColumn, QualificationOneColumn, Membership, MembershipCategory, MembershipOneColumn, Username, Catalog, Journal, JournalRegistration, JournalAttachment, IsPublic, ParentNote, Note, RegistrationNumber, YearFrom, IsUnitEnroll, UnitEnrollCondition, AllowDataStorage, AllowAudiovisual, AllowSocialNetwork, AllowMarketing, School, IdCardValidTo, IdCardNumber, ParentFatherFirstName, ParentFatherLastName, ParentFatherPhone, ParentFatherMail, ParentFatherNote, ParentMotherFirstName, ParentMotherLastName, ParentMotherMail, ParentMotherPhone, ParentMotherNote, ParentOtherFirstName, ParentOtherLastName, ParentOtherMail, ParentOtherPhone, ParentOtherNote, ParentOtherParentType, PromiseChild, PromiseScout, PromiseOfficial, TrailProgress, Person=None, DisplayName=None, Units=None, MembershipTypes=None, RegistrationMemberships=None, MembershipCategories=None, Functions=None, Qualifications=None, ViewContactTypes=None, ViewFunctions=None, ViewQualifications=None):
        return self._client.service.ExportPersonInsert({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "FunctionFilter": FunctionFilter, "FunctionAnd": FunctionAnd, "QualificationAnd": QualificationAnd, "AgeFrom": AgeFrom, "AgeTo": AgeTo, "ViewDisplayName": ViewDisplayName, "FirstName": FirstName, "LastName": LastName, "NickName": NickName, "MaidenName": MaidenName, "Birthday": Birthday, "IdentificationNumber": IdentificationNumber, "IdentificationNumberStart": IdentificationNumberStart, "Age": Age, "Sex": Sex, "IsForeign": IsForeign, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "Assurance": Assurance, "AssuranceCard": AssuranceCard, "Allergy": Allergy, "FoodRestrictions": FoodRestrictions, "Drugs": Drugs, "SpecialRequirements": SpecialRequirements, "HealthLimitation": HealthLimitation, "BodySkills": BodySkills, "FunctionOneColumn": FunctionOneColumn, "QualificationOneColumn": QualificationOneColumn, "Membership": Membership, "MembershipCategory": MembershipCategory, "MembershipOneColumn": MembershipOneColumn, "Username": Username, "Catalog": Catalog, "Journal": Journal, "JournalRegistration": JournalRegistration, "JournalAttachment": JournalAttachment, "IsPublic": IsPublic, "ParentNote": ParentNote, "Note": Note, "RegistrationNumber": RegistrationNumber, "YearFrom": YearFrom, "IsUnitEnroll": IsUnitEnroll, "UnitEnrollCondition": UnitEnrollCondition, "AllowDataStorage": AllowDataStorage, "AllowAudiovisual": AllowAudiovisual, "AllowSocialNetwork": AllowSocialNetwork, "AllowMarketing": AllowMarketing, "School": School, "IdCardValidTo": IdCardValidTo, "IdCardNumber": IdCardNumber, "ParentFatherFirstName": ParentFatherFirstName, "ParentFatherLastName": ParentFatherLastName, "ParentFatherPhone": ParentFatherPhone, "ParentFatherMail": ParentFatherMail, "ParentFatherNote": ParentFatherNote, "ParentMotherFirstName": ParentMotherFirstName, "ParentMotherLastName": ParentMotherLastName, "ParentMotherMail": ParentMotherMail, "ParentMotherPhone": ParentMotherPhone, "ParentMotherNote": ParentMotherNote, "ParentOtherFirstName": ParentOtherFirstName, "ParentOtherLastName": ParentOtherLastName, "ParentOtherMail": ParentOtherMail, "ParentOtherPhone": ParentOtherPhone, "ParentOtherNote": ParentOtherNote, "ParentOtherParentType": ParentOtherParentType, "PromiseChild": PromiseChild, "PromiseScout": PromiseScout, "PromiseOfficial": PromiseOfficial, "TrailProgress": TrailProgress, "Person": Person, "DisplayName": DisplayName, "Units": Units, "MembershipTypes": MembershipTypes, "RegistrationMemberships": RegistrationMemberships, "MembershipCategories": MembershipCategories, "Functions": Functions, "Qualifications": Qualifications, "ViewContactTypes": ViewContactTypes, "ViewFunctions": ViewFunctions, "ViewQualifications": ViewQualifications})

    # Upravit šablonu exportu osob
    def ExportPersonUpdate(self, ID_Login, ID, ID_Person, RegistrationYear, FunctionFilter, FunctionAnd, QualificationAnd, AgeFrom, AgeTo, ViewDisplayName, FirstName, LastName, NickName, MaidenName, Birthday, IdentificationNumber, IdentificationNumberStart, Age, Sex, IsForeign, Street, City, Postcode, State, PostalFirstLine, PostalStreet, PostalCity, PostalPostcode, PostalState, Assurance, AssuranceCard, Allergy, FoodRestrictions, Drugs, SpecialRequirements, HealthLimitation, BodySkills, FunctionOneColumn, QualificationOneColumn, Membership, MembershipCategory, MembershipOneColumn, Username, Catalog, Journal, JournalRegistration, JournalAttachment, IsPublic, ParentNote, Note, RegistrationNumber, YearFrom, IsUnitEnroll, UnitEnrollCondition, AllowDataStorage, AllowAudiovisual, AllowSocialNetwork, AllowMarketing, School, IdCardValidTo, IdCardNumber, ParentFatherFirstName, ParentFatherLastName, ParentFatherPhone, ParentFatherMail, ParentFatherNote, ParentMotherFirstName, ParentMotherLastName, ParentMotherMail, ParentMotherPhone, ParentMotherNote, ParentOtherFirstName, ParentOtherLastName, ParentOtherMail, ParentOtherPhone, ParentOtherNote, ParentOtherParentType, PromiseChild, PromiseScout, PromiseOfficial, TrailProgress, Person=None, DisplayName=None, Units=None, MembershipTypes=None, RegistrationMemberships=None, MembershipCategories=None, Functions=None, Qualifications=None, ViewContactTypes=None, ViewFunctions=None, ViewQualifications=None):
        return self._client.service.ExportPersonUpdate({"ID_Login": ID_Login, "ID": ID, "ID_Person": ID_Person, "RegistrationYear": RegistrationYear, "FunctionFilter": FunctionFilter, "FunctionAnd": FunctionAnd, "QualificationAnd": QualificationAnd, "AgeFrom": AgeFrom, "AgeTo": AgeTo, "ViewDisplayName": ViewDisplayName, "FirstName": FirstName, "LastName": LastName, "NickName": NickName, "MaidenName": MaidenName, "Birthday": Birthday, "IdentificationNumber": IdentificationNumber, "IdentificationNumberStart": IdentificationNumberStart, "Age": Age, "Sex": Sex, "IsForeign": IsForeign, "Street": Street, "City": City, "Postcode": Postcode, "State": State, "PostalFirstLine": PostalFirstLine, "PostalStreet": PostalStreet, "PostalCity": PostalCity, "PostalPostcode": PostalPostcode, "PostalState": PostalState, "Assurance": Assurance, "AssuranceCard": AssuranceCard, "Allergy": Allergy, "FoodRestrictions": FoodRestrictions, "Drugs": Drugs, "SpecialRequirements": SpecialRequirements, "HealthLimitation": HealthLimitation, "BodySkills": BodySkills, "FunctionOneColumn": FunctionOneColumn, "QualificationOneColumn": QualificationOneColumn, "Membership": Membership, "MembershipCategory": MembershipCategory, "MembershipOneColumn": MembershipOneColumn, "Username": Username, "Catalog": Catalog, "Journal": Journal, "JournalRegistration": JournalRegistration, "JournalAttachment": JournalAttachment, "IsPublic": IsPublic, "ParentNote": ParentNote, "Note": Note, "RegistrationNumber": RegistrationNumber, "YearFrom": YearFrom, "IsUnitEnroll": IsUnitEnroll, "UnitEnrollCondition": UnitEnrollCondition, "AllowDataStorage": AllowDataStorage, "AllowAudiovisual": AllowAudiovisual, "AllowSocialNetwork": AllowSocialNetwork, "AllowMarketing": AllowMarketing, "School": School, "IdCardValidTo": IdCardValidTo, "IdCardNumber": IdCardNumber, "ParentFatherFirstName": ParentFatherFirstName, "ParentFatherLastName": ParentFatherLastName, "ParentFatherPhone": ParentFatherPhone, "ParentFatherMail": ParentFatherMail, "ParentFatherNote": ParentFatherNote, "ParentMotherFirstName": ParentMotherFirstName, "ParentMotherLastName": ParentMotherLastName, "ParentMotherMail": ParentMotherMail, "ParentMotherPhone": ParentMotherPhone, "ParentMotherNote": ParentMotherNote, "ParentOtherFirstName": ParentOtherFirstName, "ParentOtherLastName": ParentOtherLastName, "ParentOtherMail": ParentOtherMail, "ParentOtherPhone": ParentOtherPhone, "ParentOtherNote": ParentOtherNote, "ParentOtherParentType": ParentOtherParentType, "PromiseChild": PromiseChild, "PromiseScout": PromiseScout, "PromiseOfficial": PromiseOfficial, "TrailProgress": TrailProgress, "Person": Person, "DisplayName": DisplayName, "Units": Units, "MembershipTypes": MembershipTypes, "RegistrationMemberships": RegistrationMemberships, "MembershipCategories": MembershipCategories, "Functions": Functions, "Qualifications": Qualifications, "ViewContactTypes": ViewContactTypes, "ViewFunctions": ViewFunctions, "ViewQualifications": ViewQualifications})

