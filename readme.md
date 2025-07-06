# NextGen Bank Project - Udemy courses


  <h2>About:</h2>
  <h3>Tech Stack</h3>
  <ul>
    <li>DjangoRestFramework</li>
    <li>Celery</li>
    <li>Redis</li>
    <li>PostgreSQL</li>
    <li>NGINX</li>
  </ul>

<h2>Sidenotes:</h2>


  <h3>Pros:</h3>
    <ul>
      <li>A nice way to build secrets using python</li>
      <li>Typing for functions and methods</li>
      <li>Implementation of Celery Tasks to upload images</li>
      <li>Relatively nice approach to authentication</li>
      <li>Use of Database Indexes</li>
      <li>Application knowledge such as the Luhn algorithm</li>
      <li>Admin site customization</li>
    </ul>

  <h3>Cons:</h3>
    <ul>
      <li>A TDD approach would have been better. Only testing endpoints with postman is not enough.</li>
      <li>Even though its a mock this project has a serious database design problems where there is no normalization.</li>
      <li>Tutor seems to have not much experience with DRF framework (nor with database design)</li>
      <li>Bad currency setup - As a intermediate to advanced course there are some lessons with unecessary examples.</li>
      <li>Several lessons can be skipped completely as code is available in GitHub (also, as mentioned above)</li>
    </ul>

<h3>Adaptations:</h3>
    <ul>
      <li>No settings granulation in order to not modify root project files.</li>
      <li>Use of docker secrets instead of env files, wich adds an extra layer of security for credentials.</li>
      <li>Use of alpine image instead of Debian's Bookworm, which implicates in a massive image size reduction.</li>
      <li>Different setup for Dockerfiles</li>
      <li>No GenericJsonRenderer</li>
    </ul>

<h3>Issues:</h3>
  <ul>
    <li>CharField are limited to max_length 255</li>
    <li>Unecessary scripts and functions that could be handled by the framework itself such as the
  GenericJSONRenderer (Section 10 - 54) and overriding UUIDField serializer to return a string
  which serializers.UUIDField already does.</li>
    <li>Wrong use of ModelSerializer by overriding fields to the exactly the function as
  the class, while field settings can be set with extra_kwargs Meta class field. Specially
  by not using <strong>exclude</strong> fieldset.</li>
    <li>Unecessary overriding of view functions fo perform the same process written in the mixin
  (e.g. retrieve, update, partial_update and perform_update) and since its key raise_exception=True
  perform the validation with a try:except block the extra wrapping is useless.
  Thus, overall making most part of the code unproductive.</li>
  <li>Creating a custom renderer to add the status_code field to the Response seems rather redundant
  since response objects already contain an attribute for that purpose.</li>
  </ul>

  <h2>Links</h2>

  [Original Project](https://github.com/API-Imperfect/nextgen-bank)