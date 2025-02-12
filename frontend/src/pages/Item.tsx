import Profile from '@/components/FetchCustomers'
import Ordered_item from '@/components/Ordered_Items/Ordered_item'

const Item = () => {
  return (
    <div className="min-h-screen flex">
      <div className="w-1/3 h-16 bg-white flex flex-col m-4">
      <Profile/>
      </div>
      <div className="w-1/3 h-16 bg-white flex flex-col m-4">
      </div>
      <div>
        <Ordered_item />
        
      </div>
    </div>
  )
}

export default Item
