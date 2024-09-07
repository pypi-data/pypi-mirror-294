# Formparts
An association table between [wordforms](../wordforms) and larger [forms](https://github.com/cldf/cldf/tree/master/components/forms).

## FormParts: `formparts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
`Form_ID` | `string` | The associated form.<br>References forms.csv.
`Wordform_ID` | `string` | The associated wordform.<br>References wordforms.csv.
`Index` | `string` | Specifies the position of a morph in a wordform.