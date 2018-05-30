package ListViewerTest;

static class ViewHolderItem {
    TextView name;
    TextView description;
    int position;
}

public class MainActivity extends Activity{
    ArrayList<Order> orders;
    ListView listView;
    private static CustomAdapter adapter;
    
    @Override
    public void onCreate(Bundle savedInstanceState){
        super.oncreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        orders = new ArrayList<>();
        Order newOrder = new Order("orderInfo");
        orders.add(newOrder);
        
        adapter = new CustomAdapter(orders.getApplicationContext());
        listView.setAdapter(adapter)
        
        @Override
        public View getView(int position, View convertView, ViewGroup parent){
            ViewHolder viewHolder;
            if(convertView == null){
                LayoutInflater inflater = ((Activity) mContext).getLayoutInflater();
                convertView = inflater.inflate(layoutResourceId, parent, false);
                
                viewHolder = new ViewHolderItem();
                viewHolder.name = (TextView) convertView.findViewById(R.id.order_name);
                viewHolder.description = (TextView) convertView.findViewById(R.id.order_description);
                
                convertView.setTag(viewHolder);
            }else{
                viewHolder = (ViewHolderItem) convertView.getTag();
            }
            
            Order order = orders[position];
            
            if(order != null) {
                viewHolder.name.setText(order.name);
                viewHolder.description.setText(order.description);
                                
                viewHolder.name.setTag(order.name);
                viewHolder.description.setTag(order.description);
            }
            return convertView;
        }
    }
}
