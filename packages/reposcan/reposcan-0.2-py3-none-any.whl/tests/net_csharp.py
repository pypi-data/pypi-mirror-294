import re

from helpers.Helper import Helper

text = """
    // GET /tag/{tag}/page-{page}
    [HttpGet("{tag}/page-{page:int}")]
    [HttpPost("{tag}/page-{page:long}")]
    // GET /tag/{tag}/page-{page}/xyz
    [HttpGet("{tag}/page-{page:float}/xyz")]
    public IActionResult Test1([FromRoute] string tag, [FromRoute] int? page, [FromQuery] string queryParameter1, [FromQuery] string queryParameter2)
    {
        var headerParameter1 = Request.Headers["headerParameter1"].ToString();
        var headerParameter2 = Request.Headers["headerParameter2"].ToString();
        string bodyParameter1 = null;
        string bodyParameter2 = null;
        if (HttpContext.Request.Method == "POST")
        {
            using (var reader = new StreamReader(Request.Body))
            {
                var body = reader.ReadToEnd();
                var jsonBody = JsonSerializer.Deserialize<Dictionary<string, string>>(body);
                jsonBody?.TryGetValue("bodyParameter1", out bodyParameter1);
                jsonBody?.TryGetValue("bodyParameter2", out bodyParameter2);
            }
        }
        if (Request.ContentType == "application/html")
        {
            return Content("<response><message>XML format is not supported yet</message></response>", "application/xml", System.Text.Encoding.UTF8);
        }
        else if (Request.ContentType == "application/json")
        {
            return Ok(incomes); // Return JSON response
        }
        else
        {
            return StatusCode(415, "Unsupported Media Type");
        }
    }

    // GET /tag/{tag}
    [HttpGet("{tag}")]
    public IActionResult Test2([FromRoute] string tag)
    {
        return Ok();
    }
"""
text1 = """
using System.Collections.Generic;
using ApiConventions.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ApiConventions.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ContactsController : ControllerBase
    {
        private readonly IContactRepository _contacts;

        public ContactsController(IContactRepository contacts)
        {
            _contacts = contacts;
        }

        // GET api/contacts
        [HttpGet]
        public IEnumerable<Contact> Get()
        {
            return _contacts.GetAll();
        }

        #region missing404docs
        // GET api/contacts/{guid}
        [HttpGet("{id}", Name = "GetById")]
        [ProducesResponseType(typeof(Contact), StatusCodes.Status200OK)]
        public IActionResult Get(string id)
        {
            var contact = _contacts.Get(id);

            if (contact == null)
            {
                return NotFound();
            }

            return Ok(contact);
        }
        #endregion

        // POST api/contacts
        [HttpPost]
        public IActionResult Post(Contact contact)
        {
            _contacts.Add(contact);

            return CreatedAtRoute("GetById", new { id = contact.ID }, contact);
        }

        // PUT api/contacts/{guid}
        [HttpPut("{id}")]
        public IActionResult Put(string id, Contact contact)
        {
            if (ModelState.IsValid && id == contact.ID)
            {
                var contactToUpdate = _contacts.Get(id);

                if (contactToUpdate != null)
                {
                    _contacts.Update(contact);
                    return NoContent();
                }

                return NotFound();
            }

            return BadRequest();
        }

        // DELETE api/contacts/{guid}
        [HttpDelete("{id}")]
        public IActionResult Delete(string id)
        {
            var contact = _contacts.Get(id);

            if (contact == null)
            {
                return NotFound();
            }

            _contacts.Remove(id);

            return NoContent();
        }
    }
}
"""
text2 = """
using System.Collections.Generic;
using ApiConventions.Models;
using Microsoft.AspNetCore.Mvc;

namespace ApiConventions.Controllers
{
    #region snippet_ApiConventionTypeAttribute
    [ApiController]
    [ApiConventionType(typeof(DefaultApiConventions))]
    [Route("api/[controller]")]
    public class ContactsConventionController : ControllerBase
    {
        #endregion
        private readonly IContactRepository _contacts;

        public ContactsConventionController(IContactRepository contacts)
        {
            _contacts = contacts;
        }

        // GET api/contactsconvention
        [HttpGet]
        public IEnumerable<Contact> Get()
        {
            return _contacts.GetAll();
        }

        // GET api/contactsconvention/{guid}
        [HttpGet("{id}", Name = "GetById")]
        public ActionResult<Contact> Get(string id)
        {
            var contact = _contacts.Get(id);

            if (contact == null)
            {
                return NotFound();
            }

            return Ok(contact);
        }

        // POST api/contactsconvention
        [HttpPost]
        public IActionResult Post(Contact contact)
        {
            _contacts.Add(contact);

            return CreatedAtRoute("GetById", new { id = contact.ID }, contact);
        }

        #region snippet_ApiConventionMethod
        // PUT api/contactsconvention/{guid}
        [HttpPut("{id}")]
        [ApiConventionMethod(typeof(DefaultApiConventions), 
                             nameof(DefaultApiConventions.Put))]
        public IActionResult Update(string id, Contact contact)
        {
            var contactToUpdate = _contacts.Get(id);

            if (contactToUpdate == null)
            {
                return NotFound();
            }
-
            _contacts.Update(contact);

            return NoContent();
        }
        #endregion

        // DELETE api/contactsconvention/{guid}
        [HttpDelete("{id}")]
        public IActionResult Delete(string id)
        {
            var contact = _contacts.Get(id);

            if (contact == null)
            {
                return NotFound();
            }

            _contacts.Remove(id);

            return NoContent();
        }
    }
}
"""
text3 = """
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SwaggerApp.Data;
using SwaggerApp.Models;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace SwaggerApp.Controllers
{
    [Produces("application/json")]
    [Route("[controller]")]
    public class FruitsController : ControllerBase
    {
        private readonly SampleContext _context;

        public FruitsController(SampleContext context)
        {
            _context = context;
        }

        [HttpGet]
        public ActionResult<IEnumerable<Fruit>> Get() =>
            _context.Fruits.ToList();

        [HttpGet("{id}")]
        public async Task<ActionResult<Fruit>> GetById(int id)
        {
            var fruit = await _context.Fruits.FindAsync(id);
            
            if (fruit == null)
            {
                return NotFound();
            }

            return fruit;
        }

        [HttpPost]
        public async Task<ActionResult<Fruit>> Create(Fruit fruit)
        {
            _context.Fruits.Add(fruit);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = fruit.Id }, fruit);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(int id, Fruit fruit)
        {
            if (id != fruit.Id)
            {
                return BadRequest();
            }

            _context.Entry(fruit).State = EntityState.Modified;
            await _context.SaveChangesAsync();

            return NoContent();
        }

        [HttpDelete("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesDefaultResponseType]
        public async Task<IActionResult> Delete(int id)
        {
            var fruit = await _context.Fruits.FindAsync(id);

            if (fruit == null)
            {
                return NotFound();
            }

            _context.Fruits.Remove(fruit);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}
"""
apiPattern = r'''((?:\/\/\ \w+ (?P<paths>\S+)\n)|(?:\[Http(?P<httpMethods>\w+).*\n)|(?:return StatusCode\((?P<responseCodes>\d+).*\n)|(?:(?:public |protected |private )(?:async )?\S+ (?P<functionName>\w+)\((.*(\s?(\[FromRoute\] )?\S+ (?P<pathParameters>\w+),?)*?)\)\n)|(?:(?:public |protected |private )(?:async )?\S+ \w+\((.*(\s?\[FromQuery\] \S+ (?P<queryParameters>\w+),?)*?)\)\n)|(?:Request.Headers\["(?P<headerParameters>.*)\".*\n)|(?:Request.ContentType == "(?P<contentTypes>.*)\".*\n)|.*?\n)*?(?:(?:(?P<firstSeparatorPart>.*}\n\n)(?P<secondSeparatorPart>\s*[\/\[]))|\Z)'''

# Loop all api matches
apiMatches = re.finditer(apiPattern, text)
apiMatches = [apiMatch for apiMatch in apiMatches if apiMatch.group(0).strip() != ""]
linePatterns = Helper.getLinePatterns(apiPattern)
secondSeparatorParts= [""]
for apiMatch in apiMatches:
    apiMatchResult = Helper.getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts)
    if apiMatchResult and ("paths" in apiMatchResult or "httpMethods" in apiMatchResult):
        print(apiMatchResult)
