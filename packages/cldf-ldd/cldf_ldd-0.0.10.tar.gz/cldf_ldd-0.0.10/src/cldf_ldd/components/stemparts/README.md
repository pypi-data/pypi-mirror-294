# Stemparts


## StemParts: `stemparts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
`Stem_ID` | `string` | The involved stem.<br>References stems.csv.
`Morph_ID` | `string` | The involved morph.<br>References morphs.csv.
`Index` | `string` | Specifies the position of a morph in a stem.
`Gloss_ID` | list of `string` (separated by `,`) | The gloss the morph has in the stem.<br>References glosses.csv.