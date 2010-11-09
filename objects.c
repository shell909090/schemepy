#include 'objects.h'

SNil * obj_null = NULL;

SObject * screate_nil()
{
    if(obj_null == NULL){
	obj_null = malloc(sizeof SNil);
	obj_null->type = STYPE_Nil;
	obj_null->ref_count = 1; /* will never free all. */
    }
    obj_null->ref_count++;
    return obj_null;
}

int sfree_nil(SNil * obj_nil)
{
    obj_nil->ref_count--;
    return 0;
}

SObject * screate_pair(SObject * car, SObject * cdr)
{
    SPair * obj_pair;
    obj_pair = malloc(sizeof SPair);
    obj_pair->type = STYPE_Pair;
    obj_pair->ref_count = 1;
    car->ref_count++;
    obj_pair->car = car;
    cdr->ref_count++;
    obj_pair->cdr = cdr;
    return obj_pair;
}

int sfree_pair(SPair * obj_pair)
{
    sfree(obj_pair->cdr);
    sfree(obj_pair->car);
    free(obj_pair);
    return 0;
}

SObject * screate_string(char * buf, int size)
{
    SString * obj_str;
    if(size == 0) size = strlen(buf);
    obj_str = malloc(sizeof SString);
    obj_str->type = STYPE_String;
    obj_str->ref_count =1;
    obj_str->buf = malloc(size+1);
    strcpy(obj_str->buf, buf, size);
    obj_str->buf[size] = 0;
    return obj_str;
}

int sfree_string(SString * obj_str)
{
    free(obj_str->buf);
    free(obj_str);
    return 0;
}

int sfree(SObject * obj)
{
    obj->ref_count--;
    if(obj->ref_count != 0) return 0;
    switch(obj->type){
    case STYPE_Nil: return sfree_nil(obj);
    case STYPE_Pair: return sfree_pair(obj);
    case STYPE_String: return sfree_string(obj);
    }
    return 0;
}
