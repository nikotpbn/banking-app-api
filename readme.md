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

<h2>Course Sidenotes:</h2>


  <h3>Pros:</h3>
    <ul>
      <li>A nice way to build secrets using python</li>
      <li>Typing for functions and methods</li>
      <li>Implementation of Celery Tasks to upload images</li>
      <li>Relatively nice approach to authentication</li>
      <li>Use of Database Indexes</li>
      <li>Application knowledge such as the Luhn algorithm</li>
      <li>Admin site customization</li>
      <li>Use of logs</li>
      <li>Transactions</li>
    </ul>

  <h3>Cons:</h3>
    <ul>
      <li>A TDD approach would have been better. Only testing endpoints with postman is not enough.</li>
      <li>Even though its a mock this project has a serious database design problems where there is no normalization.</li>
      <li>Tutor seems to have not much experience with DRF framework (nor with database design)</li>
      <li>Bad currency setup</li>
      <li>As a intermediate to advanced course there are several lessons with unecessary examples.</li>
    </ul>

<h2>Project Sidenotes:</h2>

<h3>Adaptations:</h3>
    <ul>
      <li>No settings granulation in order to not modify root project files.</li>
      <li>Use of docker secrets instead of env files, wich adds an extra layer of security for credentials.</li>
      <li>Use of alpine image instead of Debian's Bookworm, which implicates in a massive image size reduction.</li>
      <li>Different setup for Dockerfiles</li>
      <li>No GenericJsonRenderer</li>
      <li>Use of ModelSerializer where applicable and no overriiding of its methods</li>
      <li>Use of routers</li>
      <li>Removed redundant methods, functions and overrides</li>
    </ul>

<h3>Issues:</h3>
  <ul>
    <li><strong><span style="color:red">For almost every banking action there is an email sent which in a real scenario is unpractical</strong></span></li>
    <li>Validator do not let balance be negative (which is possible and would mean debit) </li>
    <li>CharField are limited to max_length 255</li>
    <li>Unecessary scripts and functions that could be handled by the framework itself</li>
    <li>Superfulous overriding of serializers and view methods</li>
    <li>Redundant try:catch wrapping on serializer.is_valid while using raise_exception key</li>
    <li>No use of cached sessions for better performance (used for steps in withdrawal)</l1>
  </ul>

  <h2>Links</h2>

  [Original Project](https://github.com/API-Imperfect/nextgen-bank)