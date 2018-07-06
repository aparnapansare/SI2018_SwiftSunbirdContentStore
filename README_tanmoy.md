# Content Service Apis
>  by Tanmoy Ghosh

## Changes made :
### Added routes in courseRoutes.js in routes directory

```sh
var iitbx = require('../service/iitbx')

  app.route(BASE_URL + '/iitbx/view').get(iitbx.getCoursesAPI)
  app.route(BASE_URL + '/iitbx/:course_name/view').get(iitbx.getObjectsAPI)
  app.route(BASE_URL + '/iitbx/:course_name/delete').get(iitbx.deleteCourseAPI)
  app.route(BASE_URL + '/iitbx/:course_name/:obj_name/view').get(iitbx.getParticularObjectAPI)
  app.route(BASE_URL + '/iitbx/:course_name/:obj_name/delete').get(iitbx.deleteParticularObjectAPI)
  app.use(upload.any())
  app.route(BASE_URL + '/iitbx/createcourse').post(iitbx.createCourseAPI)
```

imported the service **iitbx.js** from service directory to route the requests to the services 

### Inside **iitbx.js** all the services are defined

> - getCoursesAPI
> - getObjectsAPI
> - getParticularObjectAPI
> - deleteParticularObjectAPI
> - createCourseAPI
> - deleteCourseAPI
