# Inflectionalcategories
An inflectional category like *tense* has multiple [inflectional values](../inflectionalvalues) like *past* or *present*.

## InflCatTable: `inflectionalcategories.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | <div>             <p>A title, name or label for an entity.</p>         </div>         
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | <div>             <p>A description for an entity.</p>         </div>         
`Value_Order` | list of `string` (separated by `,`) | The order in which the values of this category should be ordered (contains inflectionalvalue IDs).