# Wordformstems


## FormStems: `wordformstems.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
`Wordform_ID` | `string` | The associated wordform.<br>References wordforms.csv.
`Stem_ID` | `string` | The stem of the associated wordform.<br>References stems.csv.
`Index` | list of `integer` (separated by `,`) | Specifies the position(s) of an stem in a wordform.