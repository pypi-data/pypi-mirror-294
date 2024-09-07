# Inflectionalvalues
Inflectional values belong to an inflectional [category](../inflectionalcategories) and have a [gloss](../glosses).

## InflValTable: `inflectionalvalues.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | <div>             <p>A title, name or label for an entity.</p>         </div>         
`Category_ID` | `string` | The inflectional category the value belongs to.<br>References inflectionalcategories.csv.
`Gloss_ID` | `string` | The gloss for the inflectional value.<br>References glosses.csv.