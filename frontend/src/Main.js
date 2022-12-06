import './Main.css';
import useState from 'react-usestateref';
import ClipLoader from "react-spinners/ClipLoader";
import {getFormattedDate, getIntegerDate} from './Util';
import DataTable from 'react-data-table-component';

const override = {
  marginLeft: "0.5em",
  marginBottom: "-0.25em"
};

/**
 * Main class which shows all news data and selection
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
function Main(props) {

    const [inputDate, setInputDate, inputDateRef] = useState(props?.value ?? getFormattedDate(new Date()));
    const [newsContent, setNewsContent] = useState([]);
    let [loading, setLoading] = useState(false);
    let selectedRelevantNews = []
    /* Column configuration */
    const columns = [
        {
            name: 'Title',
            selector: row => row.title,
            width: 30,
		    wrap: true,
        },
        {
            name: 'Content',
            selector: row => row.content,
            width: 100,
            wrap: true,
        },
        {
            name: 'Description',
            selector: row => row.description,
            width: 100,
            wrap: true,
        },
        {
            name: 'Url',
            selector: row => row.url,
            width: 100,
            wrap: true,
        },
    ];

    // This method takes the selected rows and submits relevance to server
    const handleChange = ({selectedRows}) => {
        console.log('Selected Rows: ', selectedRows);
        selectedRelevantNews = selectedRows;
    };

    const submitRelevantFeedback = () => {
        console.log('Total selected: ', selectedRelevantNews.length);
        // API call to send selected rows

        fetch('/relevance', {
          method: 'POST',
          mode: 'cors',
          headers: new Headers({'content-type': 'application/json'}),
          body: JSON.stringify(selectedRelevantNews)
        }).then(res => {
            return res.json();
        }).then(
            (result) => {
                console.log("Response from server: ", result);
           },
            (error) => {
                console.log("Error from server: ", error);
            }
          );

    }


    // Method to accept the contents
    function getNewsContent(event) {
        setInputDate(event.target.value);
        const formattedToday = getFormattedDate(new Date());
        const intToday = getIntegerDate(formattedToday);
        const intSelected = getIntegerDate(inputDateRef.current);
        if(intToday < intSelected){
            alert(`Date provided ${inputDateRef.current} is in future. Please select today or date from past!`);
            return;
        }

        setLoading(true);

        console.log("Input Date: ", inputDateRef.current);
        fetch("/news?date=" + inputDateRef.current)
          .then(res => {
              console.log(res);
              return res.json();
          })
          .then(
            (result) => {
              setLoading(false);
              setNewsContent(result);
            },
            (error) => {
                console.log(error);
                setLoading(false);
                let errorContent = [{id: 1, content: error}];
                setNewsContent(errorContent);
            }
          );
    }

    const ExpandedComponent = ({ data }) => <div className="expandedText">{data.content}</div>;

    return (
    <div className="mainContent">
        <label id={'newsDateLabel'} className="newsDateLabel">Enter date to continue: </label>
        <input type="date" name="newsDate" id="newsDate" className="newsDateInput" value={inputDate} onChange={event => getNewsContent(event)}/>

        <ClipLoader
            color="white"
            loading={loading}
            cssOverride={override}
            size={15}
            aria-label="Loading Spinner"
            data-testid="loader"
        />
        <hr/>
        <div className="newsContent">
            {newsContent['articles'] && newsContent['articles'].length > 0 &&
                <div>
                    <h4>Top Trending Topics: </h4>

                    <div>
                        {newsContent['topics'] && newsContent['topics'].map(topic =>
                            <div key={topic}>
                                <span>{topic}</span>
                                <br/>
                            </div>
                        )}
                    </div>

                    <div className="newsContentDiv">
                        <DataTable
                          columns={columns}
                          data={newsContent['articles']}
                          theme="dark"
                          highlightOnHover
                          pointerOnHover
                          pagination
                          selectableRows
                          expandableRows
                          onSelectedRowsChange={handleChange}
                          expandableRowsComponent={ExpandedComponent}
                        />
                    </div>
                    <input type="button" className="submitRelevance"  name="submitRelevance" id="submitRelevance" value="Submit Relevant Feedback" onClick={submitRelevantFeedback}/>
                </div>
            }
        </div>
    </div>
  );
}

export default Main;
