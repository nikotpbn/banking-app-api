# NextGen Bank project from Udemy course

Tech Stack:
DjangoRestFramework, Celery, Redis, PostgreSQL, NGINX

Sidenotes:
- A TDD approach would have been better. Only testing endpoints with postman is not enough.

Adaptations:
 - No settings granulation in order to not modify root project files.
 - Use of docker secrets instead of env files, wich adds an extra layer of security for credentials.
 - Use of alpine image instead of Debian's Bookworm, which implicates in a massive image size reduction.
 - Different setup for Dockerfiles
 - No GenericJsonRenderer ****

 Issues?
    *Unecessary scripts and functions that could be handled by the framework itself such as the
    GenericJSONRenderer (Section 10 - 54) and overriding UUIDField serializer to return a string
    which serializers.UUIDField already do.

    **Aparently wrong use of ModelSerializer by overriding fields to the exactly the function as
    the class, while field settings can be set with extra_kwargs Meta class field.

    *** Unecessary overriding of view functions fo perform the same process written in the mixin
   (e.g. retrieve, update, partial_update and perform_update) and since its key raise_exception=True
   perform the validation with a try:except block the extra wrapping is useless.
   Thus, overall making most part of the code unproductive.

   **** Creating a custom renderer to add the status_code field to the Response seems rather redundant
   since response objects already contain an attribute for that purpose.