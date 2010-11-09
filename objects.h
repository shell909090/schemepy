#ifndef SCHEME_OBJECTS
#define SCHEME_OBJECTS

#define SCHEME_OBJHEAD int type; int ref_count

enum STYPES{
    STYPE_Nil,
    STYPE_Pair,
    STYPE_String,
};
int sfree(SObject * obj);

struct SObject{
    SCHEME_OBJHEAD;
};

struct SNil{
    SCHEME_OBJHEAD;
};
SObject * screate_nil();

struct SPair{
    SCHEME_OBJHEAD;
    SObject * car;
    SObject * cdr;
};
SObject * screate_pair(SObject * car, SObject * cdr);

struct SString{
    SCHEME_OBJHEAD;
    char * buf;
};
SObject * screate_string(char * buf, int size);

#endif//SCHEME_OBJECTS
