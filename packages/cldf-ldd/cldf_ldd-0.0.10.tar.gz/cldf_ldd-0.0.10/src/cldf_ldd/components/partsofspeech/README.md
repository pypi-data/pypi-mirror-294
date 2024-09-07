# Parts of speech

## POSTable: `partsofspeech.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | <div>             <p>A unique identifier for a row in a table.</p>             <p>                 To allow usage of identifiers as path components of URLs                 IDs must only contain alphanumeric characters, underscore and hyphen.             </p>         </div>         <br>Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | A reference to a language (or variety) the form belongs to
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | <div>             <p>A title, name or label for an entity.</p>         </div>         
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | A human-readable description
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | <div>             <p>                 A human-readable comment on a resource, providing additional context.             </p>         </div>         
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | <div>             <p>List of source specifications, of the form &lt;source_ID&gt;[],                 e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12]             where meier2015 is a citation key in the accompanying BibTeX file.</p>         </div>         