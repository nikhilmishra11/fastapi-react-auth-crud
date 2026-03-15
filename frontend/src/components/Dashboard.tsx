import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store/store';
import { fetchItems, createItem, updateItem, deleteItem, Item } from '../store/itemSlice';
import { logout } from '../store/authSlice';
import { LogOut, Trash, Edit, Plus } from 'lucide-react';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { items, status } = useSelector((state: RootState) => state.items);
  
  const [editingItem, setEditingItem] = useState<Item | null>(null);
  const [formData, setFormData] = useState({ name: '', description: '', price: 0 });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchItems());
    }
  }, [status, dispatch]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingItem) {
      dispatch(updateItem({ id: editingItem.id, ...formData }));
    } else {
      dispatch(createItem(formData));
    }
    setFormData({ name: '', description: '', price: 0 });
    setEditingItem(null);
    setShowForm(false);
  };

  const editItem = (item: Item) => {
    setEditingItem(item);
    setFormData({ name: item.name, description: item.description || '', price: item.price });
    setShowForm(true);
  };

  return (
    <div className="dashboard-container">
      <nav className="glass-nav">
        <h2>Dashboard</h2>
        <button onClick={() => dispatch(logout())} className="btn icon-btn error-btn">
          <LogOut size={18} /> Logout
        </button>
      </nav>

      <main className="dashboard-main">
        <div className="actions-bar">
          <button onClick={() => { setShowForm(!showForm); setEditingItem(null); setFormData({name: '', description: '', price: 0})}} className="btn primary-btn">
            <Plus size={18} /> {showForm ? 'Cancel' : 'Add Item'}
          </button>
        </div>

        {showForm && (
          <div className="glass-panel form-panel">
            <h3>{editingItem ? 'Edit Item' : 'Create Item'}</h3>
            <form onSubmit={handleSubmit} className="item-form">
              <input required placeholder="Name" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
              <input placeholder="Description" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
              <input required type="number" step="0.01" placeholder="Price" value={formData.price} onChange={e => setFormData({...formData, price: parseFloat(e.target.value)})} />
              <button type="submit" className="btn success-btn">Save</button>
            </form>
          </div>
        )}

        <div className="items-grid">
          {items.map(item => (
            <div key={item.id} className="item-card glass-panel">
              <h4>{item.name}</h4>
              <p className="desc">{item.description}</p>
              <p className="price">${item.price}</p>
              <div className="item-actions">
                <button onClick={() => editItem(item)} className="btn icon-btn"><Edit size={16} /></button>
                <button onClick={() => dispatch(deleteItem(item.id))} className="btn icon-btn error-btn"><Trash size={16} /></button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
